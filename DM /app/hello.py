from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import connect, Error

app = Flask(__name__)

user_input = 'root'
# remplacez par votre mot de passe
password = 'SQLTAL49!'
dbname = 'DMCSGO4'

try:
    # on obtient une variable connection de type MySQLConnection avec laquelle on peut intéragir avec le serveur
    connection = connect(
        host="localhost",
        user = user_input,
        password = password,
        database=dbname
    )
    print(connection)

except Error as e:
    print(e)
    
@app.route('/add_term', methods=['POST'])
def add_term():
    """
    La fonction `add_term()` insère un nouveau terme et sa définition correspondante dans une table de base de données,
    ainsi que les pondérations pour les différents niveaux de compétence.
    Retour : une réponse JSON avec un message indiquant que le terme a été ajouté avec succès.
    """
    data = request.json
    terme = data['terme']
    definition = data['definition']
    poids_avance = data['poids_avance']
    poids_intermediaire = data['poids_intermediaire']
    poids_debutant = data['poids_debutant']

    
    with connection.cursor() as cursor:
            # Insérer dans la table Poids
        cursor.execute("INSERT INTO Poids (PoidsAvance, PoidsIntermediaire, PoidsDebutant) VALUES (%s, %s, %s)", (poids_avance, poids_intermediaire, poids_debutant))
        id_poids = cursor.lastrowid

            # Insérer dans la table Vocabulaire
        cursor.execute("INSERT INTO Vocabulaire (Terme, Définition, idPoids) VALUES (%s, %s, %s)", (terme, definition, id_poids))

        connection.commit()
        return jsonify({'message': 'Terme ajoute avec succes'})
    



@app.route('/delete_term/<int:id_vocabulaire>', methods=['DELETE'])
def delete_term(id_vocabulaire):
    """
    La fonction `delete_term` supprime un terme de la table Vocabulaire d'une base de données, ainsi que l'entrée correspondante dans la table Poids.
    l'entrée correspondante dans la table Poids.
    
    :param id_vocabulaire : Le paramètre `id_vocabulaire` est l'identifiant unique du terme qui doit être supprimé de la base de données.
    doit être supprimé de la base de données
    :return : une réponse JSON avec un message indiquant que le terme avec l'identifiant donné a été supprimé.
    """

    with connection.cursor() as cursor:
            # Récupérer et supprimer l'entrée de la table Vocabulaire
        cursor.execute("SELECT idPoids FROM Vocabulaire WHERE idVocabulaire = %s", (id_vocabulaire,))
        row = cursor.fetchone()
        if row is not None:
            id_poids = row[0]

            cursor.execute("DELETE FROM Vocabulaire WHERE idVocabulaire = %s", (id_vocabulaire,))
            cursor.execute("DELETE FROM Poids WHERE idPoids = %s", (id_poids,))

            connection.commit()
            return jsonify({'message': f'Terme avec id {id_vocabulaire} supprime'})
        
   
@app.route('/update_term/<int:id_vocabulaire>', methods=['PUT'])
def update_term(id_vocabulaire):
    """
    La fonction `update_term` met à jour la définition et les poids d'un terme dans la base de données en se basant sur l'identifiant du terme.
    l'ID du terme fourni.
    
    :param id_vocabulaire : Le paramètre "id_vocabulaire" est l'identifiant unique du terme dans la base de données.
    base de données. Il est utilisé pour identifier le terme spécifique qui doit être mis à jour.
    :return : une réponse JSON avec un message indiquant que le terme avec l'ID donné a été mis à jour.
    """
    
    data = request.json
    nouvelle_definition = data.get('definition')
    nouveaux_poids = data.get('poids')  # Un dictionnaire avec poids_avance, poids_intermediaire, poids_debutant

    
        
    with connection.cursor() as cursor:
            # Mise à jour de la définition dans la table Vocabulaire
        if nouvelle_definition:
            cursor.execute("UPDATE Vocabulaire SET Définition = %s WHERE idVocabulaire = %s", (nouvelle_definition, id_vocabulaire))

            # Mise à jour des poids dans la table Poids
        if nouveaux_poids:
            cursor.execute("""
                UPDATE Poids 
                SET PoidsAvance = %s, PoidsIntermediaire = %s, PoidsDebutant = %s
                WHERE idPoids = (SELECT idPoids FROM Vocabulaire WHERE idVocabulaire = %s)
                """, (nouveaux_poids['avance'], nouveaux_poids['intermediaire'], nouveaux_poids['debutant'], id_vocabulaire))

        connection.commit()
    
        return jsonify({'message': f'Terme avec id {id_vocabulaire} mis à jour'})
    

@app.route('/vocabulaire_poids', methods=['GET'])
def get_vocabulaire_poids():
    """
    La fonction `get_vocabulaire_poids` récupère les données de vocabulaire avec leurs poids
    poids correspondants de la base de données.
    return: les résultats d'une requête SQL qui joint la table "Vocabulaire" à la table "Poids". Les résultats
    résultats retournés comprennent les colonnes de la table "Vocabulaire" et les colonnes "PoidsAvance",
    "PoidsIntermediaire" et "PoidsDebutant" de la table "Poids". Les résultats sont retournés au format JSON
    au format JSON
    """
    query = """
    SELECT Vocabulaire.*,Poids.PoidsAvance , Poids.PoidsIntermediaire, Poids.PoidsDebutant
    FROM Vocabulaire
    JOIN Poids ON Vocabulaire.idPoids = Poids.idPoids
    """
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return jsonify(results)


@app.route('/get_specific_data/<int:id_vocabulaire>', methods=['GET'])
def get_specific_data(id_vocabulaire):
    """
    La fonction `get_specific_data` récupère des données spécifiques d'une base de données sur la base de l'élément donné
    `id_vocabulaire`.
    
    :param id_vocabulaire : Le paramètre "id_vocabulaire" est l'ID du terme de vocabulaire pour lequel vous
    pour lequel vous souhaitez obtenir des données spécifiques. Il est utilisé dans la requête SQL pour filtrer les résultats et extraire les données pour cet ID spécifique.
    données pour cet ID spécifique
    :return: La fonction `get_specific_data` renvoie un objet JSON contenant les données spécifiques pour l'identifiant `id_vocabab_data` donné.
    l'identifiant `id_vocabulaire` donné. Si les données sont trouvées, elles sont renvoyées sous forme de réponse JSON. Si aucune donnée n'est
    Si aucune donnée n'est trouvée pour l'ID donné, il renvoie une réponse JSON avec un message indiquant qu'aucune donnée n'a été trouvée,
    ainsi qu'un code d'état 404.
    """
    
        
    with connection.cursor(dictionary=True) as cursor:
        query = """
        SELECT Vocabulaire.idVocabulaire, Vocabulaire.Terme, Vocabulaire.Définition,
                Poids.PoidsAvance, Poids.PoidsIntermediaire, Poids.PoidsDebutant
        FROM Vocabulaire
        JOIN Poids ON Vocabulaire.idPoids = Poids.idPoids
        WHERE Vocabulaire.idVocabulaire = %s
        """
        cursor.execute(query, (id_vocabulaire,))
        result = cursor.fetchone()
        

    if result:
        return jsonify(result)
    else:
        return jsonify({'message': 'Aucune donnée trouvée pour cet ID'}), 404
    
def get_db_connection(): #Obliger de créer cette fonction sinon mon "bouton" pour rechercher ne fonctionne pas dans mon interface web
    """
    La fonction `get_db_connection()` retourne un objet de connexion à une base de données MySQL avec le
    l'hôte, l'utilisateur, le mot de passe et la base de données spécifiés.
    :return : un objet de connexion à la base de données.
    """
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='SQLTAL49!',
        database='DMCSGO4'
    )
    

@app.route('/')
def index():
    """
    La fonction "index" renvoie le modèle rendu pour le fichier "index.html".
    :return : le résultat de l'appel à la fonction `render_template('index.html')`.
    """
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    """
    La fonction `get_data` récupère les données d'une base de données en fonction d'un terme de recherche et les renvoie au format
    JSON.
    Retour : une réponse JSON contenant les données extraites de la base de données. En cas d'erreur, la fonction
    retournera une réponse JSON avec un message d'erreur et un code d'état de 500.
    """
    term = request.args.get('term', '')  # Obtenir le terme de recherche

    try:
        conn = get_db_connection()
        with conn.cursor(dictionary=True) as cursor:
            if term:
                query = """
                SELECT Vocabulaire.Terme, Poids.PoidsAvance, Poids.PoidsIntermediaire, Poids.PoidsDebutant, Vocabulaire.Définition
                FROM Vocabulaire
                JOIN Poids ON Vocabulaire.idPoids = Poids.idPoids
                WHERE Vocabulaire.Terme LIKE %s
                """
                cursor.execute(query, ('%' + term + '%',))
            else:
                query = """
                SELECT Vocabulaire.Terme, Poids.PoidsAvance, Poids.PoidsIntermediaire, Poids.PoidsDebutant, Vocabulaire.Définition
                FROM Vocabulaire
                JOIN Poids ON Vocabulaire.idPoids = Poids.idPoids
                """
                cursor.execute(query)

            data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Error as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)

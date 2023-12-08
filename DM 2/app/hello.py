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
    
def get_db_connection(): #Obliger de créer cette fonction sinon marche pas
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='SQLTAL49!',
        database='DMCSGO4'
    )
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    term = request.args.get('term', '')  # Obtenir le terme de recherche

    try:
        conn = get_db_connection()
        with conn.cursor(dictionary=True) as cursor:
            if term:
                query = """
                SELECT Vocabulaire.Terme, Poids.PoidsAvance, Poids.PoidsIntermediaire, Poids.PoidsDebutant
                FROM Vocabulaire
                JOIN Poids ON Vocabulaire.idPoids = Poids.idPoids
                WHERE Vocabulaire.Terme LIKE %s
                """
                cursor.execute(query, ('%' + term + '%',))
            else:
                query = """
                SELECT Vocabulaire.Terme, Poids.PoidsAvance, Poids.PoidsIntermediaire, Poids.PoidsDebutant
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

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
    The function `add_term()` inserts a new term and its corresponding definition into a database table,
    along with the weights for different levels of proficiency.
    :return: a JSON response with a message indicating that the term has been successfully added.
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
    The function `delete_term` deletes a term from the Vocabulaire table in a database, along with its
    corresponding entry in the Poids table.
    
    :param id_vocabulaire: The parameter `id_vocabulaire` is the unique identifier of the term that
    needs to be deleted from the database
    :return: a JSON response with a message indicating that the term with the given id has been deleted.
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
    The function `update_term` updates the definition and weights of a term in the database.
    
    :param id_vocabulaire: The parameter "id_vocabulaire" is the identifier of the term in the
    vocabulary. It is used to specify which term should be updated in the database
    :return: a JSON response with a message indicating that the term with the given id has been updated.
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
    The function `get_vocabulaire_poids` retrieves vocabulary data along with their corresponding
    weights from the database.
    :return: the results of a SQL query that joins the "Vocabulaire" table with the "Poids" table. The
    returned results include the columns from the "Vocabulaire" table and the columns "PoidsAvance",
    "PoidsIntermediaire", and "PoidsDebutant" from the "Poids" table. The results are returned in JSON
    format
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
    The function `get_specific_data` retrieves specific data from a database based on the given
    `id_vocabulaire`.
    
    :param id_vocabulaire: The parameter "id_vocabulaire" is the ID of the vocabulary term for which you
    want to retrieve specific data. It is used in the SQL query to filter the results and retrieve the
    data for that specific ID
    :return: The function `get_specific_data` returns a JSON object containing the specific data for the
    given `id_vocabulaire`. If the data is found, it returns the data as a JSON response. If no data is
    found for the given ID, it returns a JSON response with a message indicating that no data was found,
    along with a 404 status code.
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
    The function `get_db_connection()` returns a connection object to a MySQL database with the
    specified host, user, password, and database.
    :return: a database connection object.
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
    The function "index" returns the rendered template for the "index.html" file.
    :return: the result of the `render_template('index.html')` function call.
    """
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    """
    The `get_data` function retrieves data from a database based on a search term and returns it as
    JSON.
    :return: a JSON response containing the data retrieved from the database. If there is an error, it
    will return a JSON response with an error message and a status code of 500.
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

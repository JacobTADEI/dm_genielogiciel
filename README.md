# Devoir Maison de Genie Logiciel


## Exercice 1 
Dans le premier exercice nous créeons notre base de données avec un script Python. Dans un premier temps nous connectons à MySQL Workbench puis nous crééons notre base de données. 
Nous créeons ensuite nos différentes tables et y inseront des données. Notre première table se nomme "Vocabulaire" et notre deuxième table se nomme "Poids". La table "Vocabulaire" possède comme
instance "IdVocabulaire", "Terme", "Défintion", "IdPoids" et notre table "Poids" possède comme instance "IdPoids", "PoidsDébutant", "PoidsIntermédiaire", "PoidsAvancé". Nos tables possèdent toutes les deux
l'instance "IdPoids" ce qui nous permet de les lier pour accéder à des données.

## Exercice 2 
Dans le deuxième exercice nous créeons une API qui permet d'envoyer des requêtes à notre base de données et d'y accéder. Nous attribuons des routes à chacune des requêtes grâce à un fichier "hello.py"
ranger dans un dossier "app" comme le veut la norme. Cette API nous permet : 
* D'accéder à toutes les données de notre base de données
* D'ajouter de nouvelles donnéés
* De supprimer des données
* De modifier des données
* D'accéder à des données spécifiques

## Exercice 3
Dans la troisième et dernier exercice nous créeons une interface Web ave

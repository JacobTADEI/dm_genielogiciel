# Devoir Maison de Genie Logiciel
Ce projet à pour but de présenter un Devoir Maison de Master Traitement Automatique des Langues

# Données
Dans le cadre ce Master nous réalisons un mémoire sur la __Détermination du niveau d'un jouer de ***Counter-Strike : Global Offensive*** par sa maîtrise langagière__. Dans ce mémoire nous nous intéressons au poids des termes spécifiques de ***Counter-Strike : Global Offensive*** et ce pour trois niveaux que nous avons délimiter : débutant, intermédiaire, avancé. Dans ce projet, nous nous intéressons donc au poids de ces termes par niveau. Notre base de données est composée de ces informations



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
Dans la troisième et dernier exercice nous créeons une interface Web avec une visualisation dans le but de visualier nos données. 
Nous avons la présence d'une graphique, avec, en abscisse nos termes et en ordonnées leur poids. Pour chacun des termes notre graphique possède trois barres verticale qui représentent
le poids du mots pour chaque niveau. Nous avons un "bouton" qui permet de rechercher un terme spécifique pour avoir les poids de ce terme et seulement ce terme. Nous avons aussi la possibilité de choisir le poids des niveaux que l'on souhaite en barrant le niveau non-désiré dans la légende du graphique. Par exemple si on veut voir seulement les poids intermédiaire et avancé d'un mot, alors on clique sur "débutant" pour le supprimer de notre graphique. Ce graphique s'adapte aux requêtes écrites dans l'exercice 2

## Langage et frameworks
Dans ce projet, nous utilisons le langage __Python__ ainsi que les librairies associées : 
* "mysql.connector" pour pouvoir accéder à notre base de données via python"
* "Requests" pour pouvoir faire des requêtes à notre API
* "Flask" pour pouvoir créer notre APi ainsi qu'avoir un serveur de développement pour vérifier nos requêtes

Nous utilisons également le langage __HTML__ afin d'avoir une page web pour pouvoir afficher notre graphique et __CSS__ pour styliser cette page HTML.
Puis nous utilisons __JavaScript__ pour la création de notre graphique avec la bibliothèque "Chart.js" où nous nous sommes basés sur la documentation qui se trouve [ici](https://www.chartjs.org/docs/latest/getting-started/)




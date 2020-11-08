# **OC Projet 5 - OpenFoodFacts**

Repository pour le Projet 5 du parcours Développeur d'Application Python

## **Présentation**
Il s'agit d'un programme permettant à un utilisateur rechercher des produits et proposer des aliments de substitution
plus sains que celui sélectionné. Le programme s'appuie sur les données de la base OpenFoodFacts 
(https://fr.openfoodfacts.org/).

## **Parcours utilisateur**
L'utilisateur ouvre le programme, ce dernier lui affiche les choix suivantes:

    1 Choisir des aliments à substituer. 
    2 Voir mes favoris. 
    3 Quitter le programme..

L'utilisateur sélectionne 1 : Le programme pose les questions suivantes à l'utilisateur et ce dernier sélectionne les réponses :

Sélectionnez la catégorie. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant et appuie sur entrée]
Sélectionnez l'aliment. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
Le programme propose un substitut avec un meilleur nutriscore et laisse 2 choix à l'utilisateur :

    1 - Sauvegarder mon produit dans mes favoris. 
    2 - Retourner au menu principal.

L'utilisateur sélectionne 1 :  Le programme va enregistrer le résultat dans les favoris dans la base de données et revenir au menu principale.
L'utilisateur sélectionne 2 : Le programme reviens directement au menu principal


L'utilisateur sélectionne 2 : Le programme lui montre tous les favoris enregistrer dans le base de données avec les liens vers Openfoodfacts ainsi que un magasin ou le produit peut être acheté

L'utilisateur sélectionne 3 : Le programme quitte.

## **Fonctionnalités**
Recherche d'aliments dans la base Open Food Facts.
L'utilisateur interagit avec le programme dans le terminal.
Si l'utilisateur entre un caractère qui n'est pas un chiffre, le programme doit lui répéter la question.
La recherche doit s'effectuer sur une base Sql (Postgresql dans cette versions).

## **Pré-requis**
Il est nécessaire dans un premier temps de créer une base de données et de remplir les informations de connexion à cette dernière dans le fichier config.py.

## **Installation**
Afin d'avoir toutes les packages nécessaires au bon fonctionnement installer les également le fichier requirements.txt
## **Lancement de l'application**
Pour lancer l'application, il suffit simplement d'exécuter main.py. Si vous êtes dans le répertoire app/:

    python3 main.py



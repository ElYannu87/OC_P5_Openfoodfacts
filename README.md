# **OC Projet 5 - OpenFoodFacts**

Repository pour le Projet 5 du parcours Développeur d'Application Python

## **Présentation**
Il s'agit d'un programme permettant à un utilisateur rechercher des produits et proposer des aliments de substitution
plus sains que celui sélectionné. Le programme s'appuie sur les données de la base OpenFoodFacts 
(https://fr.openfoodfacts.org/).

## **Parcours utilisateur**
L'utilisateur ouvre le programme, ce dernier lui affiche les choix suivantes:

Quel aliment souhaitez-vous remplacer?
Retrouver mes aliments favoris substitués.

L'utilisateur sélectionne 1. Le programme pose les questions suivantes à l'utilisateur et ce dernier sélectionne les réponses :

Sélectionnez la catégorie. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant et appuie sur entrée]
Sélectionnez l'aliment. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
Le programme propose un substitut, sa description, un magasin ou l'acheter (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
L'utilisateur a alors la possibilité d'enregistrer le résultat dans ses favoris dans la base de données.
## **Fonctionnalités**
Recherche d'aliments dans la base Open Food Facts.
L'utilisateur interagit avec le programme dans le terminal.
Si l'utilisateur entre un caractère qui n'est pas un chiffre, le programme doit lui répéter la question.
La recherche doit s'effectuer sur une base Sql (Postgresql dans cette versions).

## **Pré-requis**
Il est nécessaire dans un premier temps de créer une base de donnée et de remplir les informations de connexion à cette dernière dans le fichier config.py.

## **Installation**
Afin d'avoir toutes les packages nécessaires au bon fonctionnement installer les également le fichier requirements.txt
## **Lancement de l'application**
Pour lancer l'application, il suffit simplement d'exécuter main.py. Si vous êtes dans le répertoire app/:

python3 main.py



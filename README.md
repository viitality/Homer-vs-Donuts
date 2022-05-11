# Homer-vs-Donuts
## Introduction
Ce repository est l'hébergement d'un projet effectué par Maryam Aarab, Mohamed Benelkater, Alexandre Corriou et Alexia Prevot, sous la tutelle de Jeanne Barthelemy.

## Objectifs
Le but de ce jeu est de permettre à Homer d'aller manger le donut présent sur une des cases de la grille. Pour cela, nous faisons appel à des notions de **reinforcment learning** et de **chaînes de Markov**. Homer apprned donc à aller jusqu'au donut par lui-même. Cet apprentissage se fait en deux étapes : 
* **Apprentissage** : Homer se déplace aléatoirement sur la grille et en déduit un chemin vers le donut. Ceci peut prendre du temps
* **Déduction** : Une fois l'apprentissage effectué, Homer tente de traverser le meilleur chemin trouvé.
Le problème est que Homer peut se tromper de mouvement et n'ira en conséquence pas sur la case où il aurait dû aller. Ceci permet d'introduire une part supplémentaire d'aléatoire dans le jeu.

## Organisation des dossiers
Il y a 4 grands dossiers :
* HomerVSDonuts-main
* Rapport_latex_Avance
* Projet_final

Le premier contient uniquement le jeu original.
Le deuxième contient les rapports écrits en latex ainsi que toutes les images nécessaires pour.
Enfin, le dernier contient une réécriture du projet qui a pour but de simplifier le code 

## Installation et lancement

Dans un terminal Linux ou Windows :  
```
git clone https://github.com/viitality/Homer-vs-Donuts
python3 Homer-vs-Donuts/reecriture/main.py
```

## Dépendances

Les librairies python suivantes sont nécessaire au fonctionnement du programme :
* pygame
* numpy
* os

## Représentation graphique du jeu 
<img width="1199" alt="Capture d’écran 2022-05-10 à 5 19 01 PM" src="https://user-images.githubusercontent.com/92668243/167663782-6ab11363-aa7e-4634-b4a6-06a300aca67b.png">


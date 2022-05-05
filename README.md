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
* HomerVSDonuts-learning
* HomerVSDonuts-main
* Rapport_latex1
* Réécriture

Le premier contient le code du jeu auquel a été rajouté notre code.
Le deuxième contient uniquement le jeu original.
Le troisième contient les rapports écrits en latex ainsi que toutes les images nécessaires pour.
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


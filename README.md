# programme de modification de fichiers rtf en docx

Le principe est de récupérer les fichiers au format rtf depuis un répertoire source, de les convertir, puis de les déposer dans un autre répertoire.

Les étapes sont les suivantes :
- appeler une fonction de récupération des fichiers en fournissant en argument le chemin du répertoire source (source_dir).
- la fonction appelée est un générateur qui va, pour chaque fichier récupéré, appeler la fonction de conversion en fournissant le chemin complet du fichier. Dans un souci d'optimisation, l'instance de word est créée dans la fonction génératrice et transmise en argument à la fonction de conversion.
- la fonction de conversion pilote une instance de Word pour ouvrir le fichier au format rtf pour ensuite l'enregistrer au format docx.
- la fonction de conversion doit également fournir à l'instance Word le chemin de destination (target_dir) à partir du nom de fichier reçu en paramètre (appel d'une fonction dédiée).

## questions en suspend et améliorations à apporter

Il faut vérifier si le programme réussit bien à enregistrer dans un répertoire différent de celui source.
J'ai rencontré ce problème dans mes premiers tests.
Si le problème se pose, il faudra alors récupérer la liste des fichiers du répertoire source dont l'extension est .rtf, puis itérer sur cette liste. Avec cette étape supplémentaire, on pourra utiliser le répertoire source comme répertoire cible sans risquer de traiter les fichiers docx venant d'être convertis.

Il faut ajouter des tests unitaires pour que l'appli soit complète :
- vérifier le nombre de fichiers convertis
- s'assurer que les répertoires sources et de destination sont bien trouvés

Il faut gérer les erreurs et les exceptions.

## conteneurisation de l'application

Plutôt que d'avoir à installer une nouvelle version de Python sur mon poste de travail, une solution serait de créer une image Docker pour faire tourner le programme.
Cette image serait basée sur une version de Python > 3.5, accompagnait de la librairie pywin32.

Voici une ébauche du Dockerfile :

```bash
# Specifies the Docker image from Python
FROM python:3.9.7-slim-bullseye

# Image descriptions
LABEL maintainer="Mickael Bula"
LABEL version="0.1"
LABEL description = "rtf to docx converter"

# Specifies the working directory
WORKDIR /converter

# Installs `pywin32` which provides access to many of the Windows APIs from Python
RUN pip install pywin32
# Create a volume
RUN mkdir /converter
```

Le container créé à partir de l'image doit être lancé avec différents volumes liés :
- un volume pour lire le script Python
- un volume pour récupérer les fichiers rtf
- un volume pour déposer les fichiers docx

L'idée est de créer un container à partir de l'image qui exécutera le script contenu dans l'hôte à travers un montage de volume.
Ce script doit lui-même lire dans un répertoire de l'hôte, ceci au moyen d'un nouveau montage, puis écrire dans un 3e volume monté.

On se déplace dans le répertoire du Dockerfile, puis on lance la construction :

```bash
docker build -t converter .
```

On se place ensuite dans le container pour exécuter le programme :

```bash
# ouverture d'un terminal dans le container
docker run -it --name rtf2docx converter /bin/bash
# au sein du container, navigation vers le programme Python et lancement de celui-ci
cd /var/www/html/converter
py converter.py
```

## Premiers tests avec Docker

Pour effectuer mes tests, j'ai récupéré une image de Python tournant sur une distribution Debian.
Afin de pouvoir ultérieurement accéder au container, j'y exécute une commande bash lors du montage.
En outre, je fais un montage de volume entre l'hôte et le container.
Le container se nomme `busy_shamir bash` :

```bash
docker run -it -v "//c/Users/bulam/Documents":/tmp/data python:3.8-slim-buster bash
```

Avec cette commande, j'accède au contenu de mon répertoire hôte au sein du container :

```bash
cd tmp/data
```

Pour sortir du container :

```bash
exit
```

Pour arrêter, puis relancer le container :

```bash
docker stop busy_shamir
docker start busy_shamir
```

Pour ouvrir à nouveau un terminal au sein du container :

```bash
docker exec -it busy_shamir bash
```

Pour exécuter une commande Python dans le container, comme par exemple lancer un des scripts du volume partagé :

```bash
root@8bb9cff76633:/tmp/data/Kaligraf# python ./converterTests.py
```

## TODO

Il faut que je me crée une image personnalisée pour faire tourner mon script en ajoutant la librairie pywin32.
Ajouter cette librairie à l'image m'évitera d'avoir à la télécharger systématiquement.

Il restera ensuite à monter les deux volumes restants (source et target) et de faire des tests avec de simples fichiers textes.

Si les tests sont concluants, on pourra passer aux véritables données rtf dès que j'aurai accès à un poste avec Word installé.
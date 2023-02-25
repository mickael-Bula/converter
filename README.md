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
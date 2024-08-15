# Combinatorial-Testing-Tools
Générateurs de données pour les tests combinatoires développé en Python.

&nbsp;&nbsp;&nbsp;&nbsp;


## generate-data.py
**generate-data.py** génère des données pour les tests combinatoires. Cet outil vise à couvrir l'ensemble des combinaisons possibles de valeurs d'entrée. Il offre un langage pour les exclusions et peut exporter les données dans divers formats.

Le script utilise un fichier de données ('data.txt') ainsi qu'un fichier pour les conditions d'exclusions ('exclusions.txt').
Ces deux fichiers sont dans le même dossier que le script Python.

Le fichier 'data.txt' constitué de champs, de types et de données. Les combinaisons sont générées avec les données de ce fichier.
Dans cet exemple, nous avons le champ 'Athlete' de type TEXT, le champ 'Age' de type INTEGER ainsi que le champ 'Taille' de type REAL.
Les données suivent les champs et si une ligne débute par un #, elle sera ignorée.


Voici un exemple du fichier 'data.txt' :
```sh
Athlete|TEXT
Gretzky
Lemieux
Messi
Ronaldo

Age|INTEGER
20
25
30
#35

Taille|REAL
1.65
#1.70
#1.75
1.80
```

&nbsp;

Le fichier 'exclusions.txt' définit les conditions à exclure des combinaisons de données.
Avec ce langage SQL, on peut utiliser des opérateurs logiques tels que AND, OR et != et des parenthèses pour définir des conditions plus complexes.
Encore une fois ici, une ligne débutant par un # ne pas considérée.


Voici un exemple du fichier 'exclusions.txt' :
```sh
Age != '20'
Athlete == "Ronaldo"
#Athlete = 'Messi'
Athlete = 'Gretzky' AND Taille != '1.8'
```

#### Fonctionnalités
- Génération de toutes les combinaisons possibles de données
- Langage SQL pour l'exclusion de ces données
- Exportation des données finales en format CSV, XML, JSON ou SQL


#### Exemples d'utilisation :
```sh
python generate-data.py
python generate-data.py csv
python generate-data.py xml
python generate-data.py json
python generate-data.py sql
```
&nbsp;&nbsp;&nbsp;&nbsp;

## generate-data-csv.py
**generate-data-csv.py** génère des données pour les tests combinatoires. Cet outil vise à couvrir l'ensemble des combinaisons possibles de valeurs d'entrée. Il offre un langage pour les exclusions et peut exporter les données dans divers formats.

Le script utilise un fichier de données ('data.csv') ainsi qu'un fichier pour les conditions d'exclusions ('exclusions.txt').
Ces deux fichiers sont dans le même dossier que le script Python.

Le fichier 'data.csv' constitué de champs, de types et de données. Les combinaisons sont générées avec les données de ce fichier.
Dans cet exemple, nous avons le champ 'Athlete' de type TEXT, le champ 'Age' de type INTEGER ainsi que le champ 'Taille' de type REAL.


Voici un exemple du fichier 'data.csv' :
```sh
Athlete;Age;Taille
TEXT;INTEGER;REAL
Gretzky;20;1.65
Lemieux;25;1.80
Messi;30;
Ronaldo;;
```

&nbsp;

Le fichier 'exclusions.txt' définit les conditions à exclure des combinaisons de données.
Avec ce langage SQL, on peut utiliser des opérateurs logiques tels que AND, OR et != et des parenthèses pour définir des conditions plus complexes.
Dans ce fichier des conditions d'exclusion, une ligne débutant par un # ne pas considérée.


Voici un exemple du fichier 'exclusions.txt' :
```sh
Age != '20'
Athlete == "Ronaldo"
#Athlete = 'Messi'
Athlete = 'Gretzky' AND Taille != '1.8'
```

#### Fonctionnalités
- Génération de toutes les combinaisons possibles de données
- Langage SQL pour l'exclusion de ces données
- Exportation des données finales en format CSV, XML, JSON ou SQL


#### Exemples d'utilisation :
```sh
python generate-data-csv.py
python generate-data-csv.py csv
python generate-data-csv.py xml
python generate-data-csv.py json
python generate-data-csv.py sql
```

## Prérequis
Assurez-vous d'avoir installé et être familiarisé avec **Python**.

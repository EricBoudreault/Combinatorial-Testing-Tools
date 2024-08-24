# Developped by eboudreault@gmail.com
# 2024-08
# coding: utf-8
import os
import sys
import datetime
import sqlite3
import xml.etree.ElementTree as ET
import json
import csv
from itertools import product

# Constantes
SPLIT = "|"
IGNORE = "#"
DATA_FILE = "data.csv"
EXCLUSIONS_FILE = "exclusions.txt"
CSV_DELIMITER = ";"

"""
    Générer un nom de fichier dynamique ou statique
"""
def get_file_name(file_format, dynamic=False):
    if dynamic:
        # Obtenir la date et l'heure courante
        now = datetime.datetime.now()

        # Préparer la date et l'heure selon le format souhaité
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")

        # Générer un nom du fichier dynamique
        file_name = f"output_{date_str}_{time_str}.{file_format}"
    else:
        # Générer un nom du fichier statique
        file_name = f"output.{file_format}"

    return file_name

"""
    Vérifier si un fichier existe
"""
def file_exists(chemin):
    return os.path.isfile(chemin)

"""
    Extraire les champs, types et données du fichier de données CSV
"""
def parse_data_file(file_path):
    try:
        fields = {}
        data = {}
        
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=CSV_DELIMITER)
            header = next(reader) # Lire l'entête (noms du champ)
            types = next(reader) # Lire le type
            
            # Initialiser les champs et les dictionnaires de données
            for field, type_ in zip(header, types):
                fields[field] = type_
                data[field] = []
            
            # Lire les données
            for row in reader:
                for field, value in zip(header, row):
                    if value: # Ajouter les valeurs renseignées seulement
                        data[field].append(value)
        
        return fields, data

    except Exception as ex:
        raise ValueError(f"Erreur pendant l'extraction des champs, types et données du fichier '{file_path}'.\n{ex}")

"""
    Extraire les exclusions en tenant compte des lignes à ignorer
"""
def parse_exclusions_file(file_path):
    try:
        with open(file_path, "r") as file:
            exclusions = [
                line.strip()
                for line in file
                if not line.startswith(IGNORE) and line.strip()
            ]

        return exclusions

    except Exception as ex:
        raise ValueError(f"Erreur pendant l'extraction des exclusions du fichier '{file_path}'.\n{ex}")

"""
    Créer la base de données en mémoire
"""
def create_database(fields):
    try:
        # Créer une connexion à une base de données SQLite en mémoire
        conn = sqlite3.connect(":memory:")

        # Créer un curseur pour interagir avec la base de données
        c = conn.cursor()

        # Préparer les champs
        columns = ', '.join([f"{field} {type_}" for field, type_ in fields.items()])

        # Créer la table avec les champs et types définis dans le fichier de données
        c.execute(f"CREATE TABLE data ({columns})")

        return conn, c

    except Exception as ex:
        raise ValueError(f"Erreur pendant la création de la base de données.\n{ex}")

"""
    Créer l'ensemble des combinaisons possibles
"""
def generate_combinations(cursor, data):
    try:
        keys = data.keys()

        # Générer les combinaisons avec « itertools »
        values = product(*data.values())

        # Insérer les combinaisons de données dans la table
        for value in values:
            cursor.execute(
                f"INSERT INTO data ({', '.join(keys)}) VALUES ({', '.join(['?' for _ in keys])})",
                value,
            )

    except Exception as ex:
        raise ValueError(f"Erreur pendant la génération des combinaisons de données.\n{ex}")

"""
    Exécuter des requêtes SQL pour supprimer les enregistrements correspondant aux exclusions
"""
def apply_exclusions(cursor, exclusions):
    for exclusion in exclusions:
        if exclusion and not exclusion.startswith(IGNORE):
            exclusion = exclusion.strip()

            try:
                cursor.execute(f"DELETE FROM data WHERE {exclusion}")

            except Exception as ex:
                print(f"La ligne '{exclusion}' est erronée et ne sera pas prise en compte.\n{ex}")
                continue

"""
    Exporter la table vers un fichier XML
"""
def export_table_to_xml(cursor, output_file):
    try:
        # Exécuter une requête pour récupérer les données de la table
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()

        # Récupérer les noms des colonnes
        column_names = [description[0] for description in cursor.description]

        # Création de l'élément racine pour l'XML
        root = ET.Element("table", name="data")

        # Parcourir les lignes de la table et les ajouter à l'XML
        for row in rows:
            row_elem = ET.SubElement(root, "row")

            for col_name, col_value in zip(column_names, row):
                col_elem = ET.SubElement(row_elem, col_name)
                col_elem.text = str(col_value)

        # Créer un arbre XML et l'écrire dans un fichier
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

    except Exception as ex:
        raise ValueError(f"Erreur pendant l'exportation de la table en XML.\n{ex}")

"""
    Exporter la table vers un fichier JSON
"""
def export_table_to_json(cursor, output_file):
    try:

        # Exécuter une requête pour récupérer les données de la table
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()

        # Récupérer les noms des colonnes
        column_names = [description[0] for description in cursor.description]

        # Créer une liste de dictionnaires représentant les lignes de la table
        data = []

        for row in rows:
            row_dict = {
                col_name: col_value for col_name, col_value in zip(column_names, row)
            }
            data.append(row_dict)

        # Écrire les données restantes dans un fichier JSON
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    except Exception as ex:
        raise ValueError(f"Erreur pendant l'exportation de la table en JSON.\n{ex}")

"""
    Exporter le contenu de la table vers un fichier SQL
"""
def export_table_to_sql(cursor, output_file):
    try:
        # Récupérer les données de la table
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()

        # Obtenir les noms de colonnes
        column_names = [description[0] for description in cursor.description]

        with open(output_file, 'w') as f:
            for row in rows:
                # Construire la commande INSERT INTO
                values = ', '.join(map(repr, row))
                insert_stmt = f"INSERT INTO nom_table ({', '.join(column_names)}) VALUES ({values});\n"
                f.write(insert_stmt)

    except Exception as ex:
        raise ValueError(f"Erreur pendant l'exportation du contenu de la table en SQL.\n{ex}")

"""
    Exporter la table vers un fichier CSV
"""
def export_table_to_csv(cursor, output_file):
    try:
        # Exécuter une requête pour récupérer les données de la table
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()

        # Préparer les entêtes
        headers = [description[0] for description in cursor.description]

        # Écrire les lignes et colonnes de la table
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file, delimiter=CSV_DELIMITER)
            writer.writerow(headers)
            writer.writerows(rows)

    except Exception as ex:
        raise ValueError(f"Erreur pendant l'exportation de la table en CSV.\n{ex}")

"""
    Main function
"""
def main():
    try:
        conn = None

        # S'assurer de la présence du fichier de données
        if not file_exists(DATA_FILE):
            raise ValueError(f"Le fichier des données ({DATA_FILE}) n'existe pas!")

        # S'assurer de la présence du fichier des exclusions
        if not file_exists(EXCLUSIONS_FILE):
            raise ValueError(f"Le fichier des exclusions ({EXCLUSIONS_FILE}) n'existe pas!")

        # Analyser le fichier de données et extraire les champs, types puis données correspondantes en tenant compte des lignes à ignorer
        fields, data = parse_data_file(DATA_FILE)

        # Extraire les exclusions en tenant compte des lignes à ignorer
        exclusions = parse_exclusions_file(EXCLUSIONS_FILE)

        # Créer la base de données SQLite en mémoire
        conn, cursor = create_database(fields)

        # Générer l'ensemble des combinaisons possibles
        generate_combinations(cursor, data)

        # Appliquer les exclusions
        apply_exclusions(cursor, exclusions)

        # Récupérer l'argument pour générer le fichier du format demandé
        if len(sys.argv) == 1:
            file_format = "csv"
        else:
            file_format = sys.argv[1].lower()

        # Générer un nom du fichier dynamique ou statique
        output_file = get_file_name(file_format, False)

        # Exporter la table vers le format demandé
        if file_format == "xml":
            export_table_to_xml(cursor, output_file)
        elif file_format == "json":
            export_table_to_json(cursor, output_file)
        elif file_format == "sql":
            export_table_to_sql(cursor, output_file)
        else:
            export_table_to_csv(cursor, output_file)

    except Exception as ex:
        print(f"{ex}")

    finally:

        # Fermer la connexion, si nous sommes toujours connectés à la base de données
        if conn:
            conn.close()

"""
    Entry Point
"""
if __name__ == "__main__":
    main()

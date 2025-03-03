from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType
import gzip
import xml.etree.ElementTree as ET

# Créer une session Spark
spark = SparkSession.builder \
    .appName("Discogs Duration Calculation") \
    .getOrCreate()

# Fonction pour extraire la durée d'un morceau (en secondes) à partir d'un XML
def parse_duration(xml_string):
    try:
        # Parser l'XML
        root = ET.fromstring(xml_string)
        total_duration = 0
        # Trouver les balises <tracklist> et leurs <track> 
        for track in root.iter("track"):
            duration_elem = track.find("duration")
            if duration_elem is not None and duration_elem.text:
                duration_text = duration_elem.text.strip()
                minutes, seconds = map(int, duration_text.split(":"))
                total_duration += minutes * 60 + seconds
        return total_duration
    except Exception as e:
        return 0  # Retourne 0 si une erreur survient

# Enregistrer la fonction UDF pour PySpark
parse_duration_udf = udf(parse_duration, IntegerType())

# Fonction de lecture ligne par ligne à partir du fichier .gz
def read_gzipped_file(file_path, chunk_size=10000):
    with gzip.open(file_path, 'rt') as f:
        current_chunk = []
        for line in f:
            current_chunk.append(line.strip())
            if len(current_chunk) >= chunk_size:
                yield current_chunk
                current_chunk = []
        # Dernier lot s'il en reste
        if current_chunk:
            yield current_chunk

# Charger le fichier XML compressé et traiter par morceaux de 10 000 lignes
file_path = "../../discogs_20250301_releases.xml.gz"
chunk_size = 10000  # Taille du lot de 10 000 lignes

# Initialiser un compteur pour la durée totale
total_duration_global = 0

# Traiter chaque lot de 10 000 lignes
for chunk_index, chunk in enumerate(read_gzipped_file(file_path, chunk_size)):
    print(f"Traitement du lot {chunk_index + 1}...")
    
    # Créer un RDD à partir du chunk
    rdd = spark.sparkContext.parallelize(chunk)
    
    # Convertir l'RDD en DataFrame pour appliquer l'UDF
    df = rdd.map(lambda x: (x,)).toDF(["xml"])

    # Appliquer l'UDF pour calculer la durée
    df_with_duration = df.withColumn("total_duration", parse_duration_udf(df["xml"]))

    # Calculer la durée totale locale en additionnant toutes les durées
    total_duration_df = df_with_duration.agg({"total_duration": "sum"})

    # Exécuter l'action pour obtenir la somme totale pour ce lot
    total_duration = total_duration_df.collect()[0][0]

    # Ajouter la durée du lot courant à la durée totale globale
    total_duration_global += total_duration

    # Afficher la durée totale pour ce lot
    total_minutes = total_duration // 60
    total_seconds = total_duration % 60
    print(f"Durée totale pour le lot {chunk_index + 1}: {total_minutes} min {total_seconds} s")

# Afficher la durée totale globale à la fin
total_minutes_global = total_duration_global // 60
total_seconds_global = total_duration_global % 60
print(f"Durée totale de toutes les musiques : {total_minutes_global} min {total_seconds_global} s")

# Arrêter la session Spark
spark.stop()

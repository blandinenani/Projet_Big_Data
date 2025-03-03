import gzip

# Fichier Discogs publié au 1er mars 2025
file_path = "../../discogs_20250301_releases.xml.gz"


with gzip.open(file_path, 'rt') as f:
    for i, line in enumerate(f):
        if i < 10:  
            print(line.strip())  
        else:
            break
import gzip
import xml.etree.ElementTree as ET

# Fichier Discogs décompressé publié au 1er mars 2025
file_path = "discogs_20250301_releases.xml.gz"

with gzip.open(file_path, 'rb') as f:
    context = ET.iterparse(f, events=("start",))
    
    structure = {}
    
    for event, elem in context:
        parent_tag = elem.tag
        if parent_tag not in structure:
            structure[parent_tag] = set()
        
        # Ajouter les sous-éléments rencontrés
        for child in elem:
            structure[parent_tag].add(child.tag)
        
        if len(structure) > 10:  # Limite pour éviter de tout parcourir
            break

# Affichage de la structure
for parent, children in structure.items():
    print(f"{parent}: {', '.join(children)}")

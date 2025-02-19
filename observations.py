import xml.etree.ElementTree as ET

# Charger le fichier XML
xml_file = "partiel_release.xml"

# Lire le contenu du fichier
with open(xml_file, "r", encoding="utf-8") as f:
    for _ in range(20):
        print(f.readline().strip())
tree = ET.parse(xml_file)
root = tree.getroot()

# Afficher les principaux éléments XML
print(f"Racine : {root.tag}")
for child in root[:5]:
    print(f"Tag: {child.tag}, Attributs: {child.attrib}")

tags = set()
for elem in root.iter():
    tags.add(elem.tag)

print("Tags uniques trouvés :", tags)


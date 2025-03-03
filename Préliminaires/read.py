import gzip
import xml.etree.ElementTree as ET

# Fichier Discogs publié au 1er mars 2025
file_path = "discogs_20250301_releases.xml.gz"

with gzip.open(file_path, 'rb') as f:
    context = ET.iterparse(f, events=("start", "end"))

    releases = []
    current_release = {}

    for event, elem in context:
        if event == "start":
            if elem.tag == "release":
                current_release = {
                    "id": elem.attrib.get("id", ""),
                    "title": "",
                    "country": "N/A",
                    "released": "N/A",
                    "genres": set(),
                    "styles": set(),
                    "labels": set(),
                    "artists": set(),
                }

            elif elem.tag == "title":
                current_release["title"] = elem.text or "Unknown"

            elif elem.tag == "country":
                current_release["country"] = elem.text or "N/A"

            elif elem.tag == "genre":
                if elem.text:
                    current_release["genres"].add(elem.text)

            elif elem.tag == "style":
                if elem.text:
                    current_release["styles"].add(elem.text)

            elif elem.tag == "artist":
                name_elem = elem.find("name")
                if name_elem is not None and name_elem.text:
                    current_release["artists"].add(name_elem.text)

            elif elem.tag == "labels":
                # Si la balise 'labels' existe, itérer sur les sous-éléments <label>
                for label_elem in elem.findall("label"):
                    # Extraire l'attribut 'name' du label
                    label_name = label_elem.attrib.get("name", "").strip()
                    if label_name:
                        current_release["labels"].add(label_name)

        elif event == "end" and elem.tag == "release":
            # Conversion des sets en liste pour éviter les doublons et afficher proprement
            current_release["artists"] = list(current_release["artists"])
            current_release["genres"] = list(current_release["genres"])
            current_release["styles"] = list(current_release["styles"])
            current_release["labels"] = list(current_release["labels"])

            releases.append(current_release)
            if len(releases) >= 10:
                break  # On s'arrête après 10 releases

            elem.clear()  # Libérer la mémoire

# Affichage des 10 premières releases
for i, release in enumerate(releases, 1):
    print(f"{i}. {release['title']} ({release['country']})")
    print(f"   Artistes: {', '.join(release['artists'])}")
    print(f"   Genres: {', '.join(release['genres'])}")
    print(f"   Styles: {', '.join(release['styles'])}")
    print(f"   Maison de disque/Label: {', '.join(release['labels']) if release['labels'] else 'Aucun label'}")
    print("-" * 80)

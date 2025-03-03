import gzip
import xml.etree.ElementTree as ET

# Fichier Discogs publié au 1er mars 2025
file_path = "discogs_20250201_releases.xml.gz"

with gzip.open(file_path, 'rb') as f:
    context = ET.iterparse(f, events=("start", "end"))

    releases = []
    current_release = {}
    inside_tracklist = False

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
                    "total_duration": 0,
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
                for label_elem in elem.findall("label"):
                    label_name = label_elem.attrib.get("name", "").strip()
                    if label_name:
                        current_release["labels"].add(label_name)

            elif elem.tag == "tracklist":
                inside_tracklist = True

            elif inside_tracklist and elem.tag == "track":
                duration_elem = elem.find("duration")
                if duration_elem is not None and duration_elem.text:
                    duration_text = duration_elem.text.strip()
                    
                    # Convertir le format "mm:ss" en secondes
                    try:
                        minutes, seconds = map(int, duration_text.split(":"))
                        current_release["total_duration"] += minutes * 60 + seconds
                    except ValueError:
                        pass  

        elif event == "end":
            if elem.tag == "tracklist":
                inside_tracklist = False  

            elif elem.tag == "release":
                current_release["artists"] = list(current_release["artists"])
                current_release["genres"] = list(current_release["genres"])
                current_release["styles"] = list(current_release["styles"])
                current_release["labels"] = list(current_release["labels"])

                releases.append(current_release)
                if len(releases) >= 10:
                    break  
                elem.clear()  

# Affichage des 10 premières releases avec la durée totale
for i, release in enumerate(releases, 1):
    print(f"{i}. {release['title']} ({release['country']})")
    print(f"   Artistes: {', '.join(release['artists'])}")
    print(f"   Genres: {', '.join(release['genres'])}")
    print(f"   Styles: {', '.join(release['styles'])}")
    print(f"   Maison de disque/Label: {', '.join(release['labels']) if release['labels'] else 'Aucun label'}")
    
    # Affichage de la durée totale en minutes et secondes
    total_minutes = release["total_duration"] // 60
    total_seconds = release["total_duration"] % 60
    print(f"   Durée totale: {total_minutes} min {total_seconds} s")
    
    print("-" * 80)

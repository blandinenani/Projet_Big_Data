# Dataset
Lien vers le dataset : https://discogs-data-dumps.s3.us-west-2.amazonaws.com/index.html?prefix=data/2025/ (discogs_20250201_releases.xml.gz)
Puis on décompresse partiellement


# Etapes 
## 1. Comprehension du dataset

1. Decompression partielle
   ```bash
   zcat discogs_20250201_releases.xml.gz | head -n 1000 > partiel_release.xml
   ```
   /!\ Ajouter "\</releases>" à la fin  de la decompression partielle /!\

2. Observation
   
    Racine : releases
    Tag: release, Attributs: {'id': '1', 'status': 'Accepted'}
    Tag: release, Attributs: {'id': '2', 'status': 'Accepted'}
    Tag: release, Attributs: {'id': '3', 'status': 'Accepted'}
    Tag: release, Attributs: {'id': '4', 'status': 'Accepted'}
    Tag: release, Attributs: {'id': '5', 'status': 'Accepted'}
    Tags uniques trouvés : {'videos', 'release', 'label', 'anv', 'video', 'companies', 'resource_url', 'identifier', 'tracks', 'formats', 'descriptions', 'entity_type_name', 'labels', 'data_quality', 'artists', 'master_id', 'join', 'identifiers', 'artist', 'role', 'tracklist', 'notes', 'genres', 'id', 'name', 'title', 'genre', 'country', 'track', 'released', 'series', 'position', 'entity_type', 'duration', 'extraartists', 'releases', 'format', 'style', 'styles', 'catno', 'company', 'description'}

## 2. Mise en place d’un job simple sur Hadoop sur le data set 

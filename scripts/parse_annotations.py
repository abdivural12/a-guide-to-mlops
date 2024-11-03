import json
import shutil
from pathlib import Path

# Chemins de dossiers constants
EXTRA_DATA_FOLDER_PATH = Path("extra-data/extra_data")
NEW_DATA_FOLDER_PATH = Path("data/raw")

# Lire les annotations et copier les images dans les dossiers annotés
with open("extra-data/annotations.json") as f:
    annotations = json.load(f)

for annotation in annotations:
    # Extraire le chemin de l'image et l'annotation
    filename = "".join(annotation["data"]["image"].split("/")[-1].split("-")[1:])
    choice = annotation["annotations"][0]["result"][0]["value"]["choices"][0]

    source_path = EXTRA_DATA_FOLDER_PATH / filename
    dest_path = NEW_DATA_FOLDER_PATH / choice / filename

    # Créez le dossier de destination s'il n'existe pas
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Copie de {source_path} -> {dest_path}")
    shutil.copy(source_path, dest_path)

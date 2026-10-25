# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""
from PIL import Image
import os
try:
    import cfg
except ImportError:
    cfg = None


class ImageData:
    def __init__(self):
        self._data = {}
        self._uuid_to_file = {}

    def add_image(self, uuid: str, file: str) -> None:
        if not os.path.isfile(file):
            print(f"File not found: {file}")
        self._uuid_to_file[uuid] = file
        if uuid not in self._data:
            self._data[uuid] = {}

    def remove_image(self, uuid: str) -> None:
        """Elimina una imagen y sus metadatos."""
        self._data.pop(uuid, None)
        self._uuid_to_file.pop(uuid, None)

    def load_metadata(self, uuid: str) -> None:
        """Lee metadatos embebidos en el PNG y los guarda."""
        file = self._uuid_to_file.get(uuid)
        if not file or not os.path.isfile(file):
            print(f"[ERROR] Cannot load metadata, file not found for UUID: {uuid}")
            return

        try:
            with Image.open(file) as img:
                info = img.text  # metadatos embebidos
                self._data[uuid] = {
                    "prompt": info.get("Prompt", None),
                    "model": info.get("Model", None),
                    "seed": info.get("Seed", None),
                    "cfg_scale": info.get("CFG_Scale", None),
                    "steps": info.get("Steps", None),
                    "sampler": info.get("Sampler", None),
                    "generated": info.get("Generated", None),
                    "created": info.get("Created_Date", None),
                    "width": str(img.width),
                    "height": str(img.height)
                }
        except Exception as e:
            print(f"[ERROR] Failed to read metadata from {file}: {e}")

    def get_prompt(self, uuid: str):
        v = self._data.get(uuid, {}).get("prompt", "None")
        return None if v == "None" else v

    def get_model(self, uuid: str):
        v = self._data.get(uuid, {}).get("model", "None")
        return None if v == "None" else v

    def get_seed(self, uuid: str):
        v = self._data.get(uuid, {}).get("seed", "None")
        return None if v == "None" else v

    def get_cfg_scale(self, uuid: str):
        v = self._data.get(uuid, {}).get("cfg_scale", "None")
        return None if v == "None" else v

    def get_steps(self, uuid: str):
        v = self._data.get(uuid, {}).get("steps", "None")
        return None if v == "None" else v

    def get_sampler(self, uuid: str):
        v = self._data.get(uuid, {}).get("sampler", "None")
        return None if v == "None" else v

    def get_generated(self, uuid: str):
        v = self._data.get(uuid, {}).get("generated", "None")
        return None if v == "None" else v

    def get_created_date(self, uuid: str):
        v = self._data.get(uuid, {}).get("created", "None")
        return None if v == "None" else v

    def get_dimensions(self, uuid: str):
        d = self._data.get(uuid, {})
        w = d.get("width", "None")
        h = d.get("height", "None")
        if w == "None" or h == "None" or w is None or h is None:
            return None
        try:
            return (int(w), int(h))
        except Exception:
            return None

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return f"ImageData: {len(self._data)} files listed."

# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""

# -*- coding: utf-8 -*-
import json
import os
try:
    import cfg
except ImportError:
    cfg = None


class Gallery:
    __slots__ = ['_name', '_description', '_created', '_uuids', '_image_id', '_image_viewer']

    def __init__(self, image_id, image_viewer):
        self._name = ""
        self._description = ""
        self._created = ""
        self._uuids = []
        self._image_id = image_id
        self._image_viewer = image_viewer

    def load_file(self, file: str) -> None:
        """Carga una galería desde un archivo JSON."""
        self._uuids.clear()

        if not os.path.isfile(file):
            return

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return

        self._name = data.get("gallery_name", "Unnamed Gallery")
        self._description = data.get("description", "No description")
        self._created = data.get("created_date", "Unknown date")

        for path in data.get("images", []):
            # normalizar path
            if cfg and hasattr(cfg, "get_canonical_pathfile"):
                try:
                    path = cfg.get_canonical_pathfile(path)
                except Exception:
                    path = os.path.normpath(os.path.abspath(path))
            else:
                path = os.path.normpath(os.path.abspath(path))

            uuid = self._image_id.get_uuid(path)
            if uuid:
                self._uuids.append(uuid)

    def show(self) -> None:
        if not self._uuids:
            print("[INFO] Gallery is empty.")
            return

        print(f"\n=== Gallery: {self._name} ===")
        print(f"Description: {self._description}")
        print(f"Created: {self._created}\n")

        for uid in self._uuids:
            self._image_viewer.show_image(uid, mode=1)

    def add_image_at_end(self, uuid: str) -> None:
        self._uuids.append(uuid)

    def remove_first_image(self) -> None:
        if self._uuids:
            self._uuids.pop(0)

    def remove_last_image(self) -> None:
        if self._uuids:
            self._uuids.pop()

    def __len__(self):
        return len(self._uuids)

    def __str__(self):
        return f"Gallery({self._name}): {len(self._uuids)} images"
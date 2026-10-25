# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""

import uuid

try:
    import cfg
except ImportError:
    cfg = None



class ImageID:
    __slots__ = ['__file_to_uuid', '__uuid_to_file']

    def __init__(self):
        self.__file_to_uuid = {}   
        self.__uuid_to_file = {}  

    def generate_uuid(self, file: str) -> str:
        if file in self.__file_to_uuid:
            print(f"[ERROR] UUID already generated for file: {file}")
            return None
        if cfg and hasattr(cfg, "get_uuid"):
            new_uuid = str(cfg.get_uuid(file))
        else:
            new_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, file))
        if new_uuid in self.__uuid_to_file:
            print(f"[ERROR] UUID collision detected for file: {file}")
            return None
        self.__file_to_uuid[file] = new_uuid
        self.__uuid_to_file[new_uuid] = file
        return new_uuid

    def get_uuid(self, file: str) -> str:
        return self.__file_to_uuid.get(file, None)

    def remove_uuid(self, uuid_str: str) -> None:
        file = self.__uuid_to_file.pop(uuid_str, None)
        if file is not None:
            del self.__file_to_uuid[file]

    def __len__(self):
        return len(self.__uuid_to_file)

    def __str__(self):
        return f"ImageID: {len(self.__uuid_to_file)} IDs generated."

    def __repr__(self):
        return f"ImageID({self.__file_to_uuid})"

    def __iter__(self):
        return iter(self.__file_to_uuid)
# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""

import os
try:
    import cfg
except ImportError:
    cfg = None


class ImageFiles:
    def __init__(self, root_dir="."):
        # Si existe cfg y tiene función, úsala
        if cfg and hasattr(cfg, "get_canonical_pathfile"):
            self.root_dir = cfg.get_canonical_pathfile(root_dir)
        else:
            self.root_dir = os.path.abspath(root_dir)

        self._files_prev = set()
        self._files_curr = set()
        self._added = []
        self._removed = []

    def _list_png_files(self, path):
        """Retorna una llista de tots els fitxers PNG dins del path."""
        png_files = []
        if not os.path.isdir(path):
            return png_files

        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                if f.lower().endswith(".png"):
                    full_path = os.path.join(dirpath, f)
                    if cfg and hasattr(cfg, "get_canonical_pathfile"):
                        rel_path = cfg.get_canonical_pathfile(full_path)
                    else:
                        rel_path = os.path.relpath(full_path, self.root_dir).replace(os.sep, "/")
                    png_files.append(rel_path)
        return png_files

    def reload_fs(self, path="."):
        """Recorre el directori i actualitza la llista d'arxius PNG."""
        if path is None:
            path = self.root_dir

        # Guarda l'estat anterior
        self._files_prev = self._files_curr.copy()

        # Carrega els nous fitxers
        new_files = self._list_png_files(path)
        self._files_curr = set(new_files)

        # Detecta canvis
        self._added = sorted(list(self._files_curr - self._files_prev))
        self._removed = sorted(list(self._files_prev - self._files_curr))

    def files_added(self):
        """Retorna la llista d'arxius afegits."""
        return self._added

    def files_removed(self):
        """Retorna la llista d'arxius eliminats."""
        return self._removed

    def __str__(self):
        return f"ImageFiles: {len(self._files_curr)} files listed."
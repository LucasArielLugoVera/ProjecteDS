# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""


#import cfg
class SearchMetadata:
    __slots__ = ['_metadata']

    def __init__(self, metadata=None):
        if hasattr(metadata, "_data"):
            self._metadata = metadata._data
        elif isinstance(metadata, dict):
            self._metadata = metadata
        else:
            self._metadata = {}

    def _search(self, field: str, sub) -> list:
        if sub is None:
            return []
        sub_str = str(sub)
        if sub_str == "":
            return []

        results = []
        for uuid, data in self._metadata.items():
            if not isinstance(data, dict):
                continue
            value = str(data.get(field, ""))
            if sub_str in value:
                results.append(uuid)
        return sorted(results)

    def prompt(self, sub) -> list:
        return self._search("prompt", sub)

    def model(self, sub) -> list:
        return self._search("model", sub)

    def seed(self, sub) -> list:
        return self._search("seed", sub)

    def cfg_scale(self, sub) -> list:
        return self._search("cfg_scale", sub)

    def steps(self, sub) -> list:
        return self._search("steps", sub)

    def sampler(self, sub) -> list:
        return self._search("sampler", sub)

    def date(self, sub) -> list:

        return self._search("created", sub)

    def and_operator(self, list1, list2):
        return sorted(set(list1) & set(list2))

    def or_operator(self, list1, list2):
        return sorted(set(list1) | set(list2))

    def __len__(self):
        return len(self._metadata)

    def __str__(self):
        return f"SearchMetadata: {len(self._metadata)} metadata elements."
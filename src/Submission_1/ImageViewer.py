# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració

Mètodes a implementar:
    - print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu

    - show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

    - show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""
from PIL import Image
import os
try:
    import cfg
except ImportError:
    cfg = None

class ImageViewer:
    __slots__ = ['_image_data']

    def __init__(self, image_data=None):
        """
        image_data: instància de ImageData (pot ser None)
        """
        self._image_data = image_data

    # -----------------------------------------------------------
    def print_image(self, uuid: str) -> None:
        if self._image_data is None or uuid not in self._image_data._uuid_to_file:
            print(f"[ERROR] No metadata found for UUID: {uuid}")
            return

        d = self._image_data
        file = d._uuid_to_file.get(uuid, "Unknown")

        # Get metadata
        prompt = d.get_prompt(uuid)
        model = d.get_model(uuid)
        seed = d.get_seed(uuid)
        cfg_scale = d.get_cfg_scale(uuid)
        steps = d.get_steps(uuid)
        sampler = d.get_sampler(uuid)
        generated = d.get_generated(uuid)
        created = d.get_created_date(uuid)

        # --- FIX DIMENSIONS ---
        dims = d.get_dimensions(uuid)
        if dims is None:
            width, height = ("None", "None")
        else:
            width, height = dims

        # Truncate long prompts
        if isinstance(prompt, str) and len(prompt) > 100:
            prompt = prompt[:97] + "..."

        print(f"UUID:         {uuid}")
        print(f"Path:         {file}")
        print(f"Dimensions:   {width}x{height}")
        print(f"Prompt:       {prompt}")
        print(f"Model:        {model}")
        print(f"Seed:         {seed}")
        print(f"CFG Scale:    {cfg_scale}")
        print(f"Steps:        {steps}")
        print(f"Sampler:      {sampler}")
        print(f"Generated:    {generated}")
        print(f"Created Date: {created}")

    def show_file(self, file: str) -> None:
        """Mostra una imatge en pantalla (asíncrona)."""
        try:
            if not os.path.isfile(file):
                print(f"[ERROR] File not found: {file}")
                return
            img = Image.open(file)
            img.show()
        except Exception as e:
            print(f"[ERROR] Could not open image '{file}': {e}")

    def show_image(self, uuid: str, mode: int) -> None:
        """
        Combina print_image() i show_file() segons el mode:
            0 → només metadades
            1 → metadades + imatge
            2 → només imatge
        """
        if self._image_data is None:
            print("[ERROR] No image data available.")
            return

        file = self._image_data._uuid_to_file.get(uuid)
        if not file:
            print(f"[ERROR] File not found for UUID: {uuid}")
            return

        if mode == 0:
            self.print_image(uuid)
        elif mode == 1:
            self.print_image(uuid)
            self.show_file(file)
            input("Press Enter to close...")
        elif mode == 2:
            self.show_file(file)
            input("Press Enter to close...")
        else:
            print(f"[ERROR] Invalid mode: {mode}")

    def __len__(self):
        return len(self._image_data) if self._image_data else 0

    def __str__(self):
        n = len(self._image_data) if self._image_data else 0
        return f"ImageViewer: {n} images ready."
# -*- coding: utf-8 -*-
"""
p1_main.py : ** OPTIONAL ** Si heu fet un main vostre, poseu aquí el codi.
                            Aquest arxiu no s'avalua automàticament.

Aquí podeu posar el vostre codi de proves per testejar les funcionalitats
implementades.

Exemples d'ús:
    - Carregar la col·lecció d'imatges
    - Generar UUID per a totes les imatges
    - Llegir metadades d'algunes imatges
    - Visualitzar imatges
    - Carregar i mostrar galeries
    - Fer cerques i crear galeries a partir dels resultats
"""
# -*- coding: utf-8 -*-
import os
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata# -*- coding: utf-8 -*-
import os
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata
import cfg


def main():
    img_files = ImageFiles(cfg.ROOT_DIR)
    img_ids = ImageID()
    img_data = ImageData()
    img_viewer = ImageViewer(img_data)

    searcher = SearchMetadata(img_data._data)

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Llistat d’imatges PNG del filesystem")
        print("2. Generació d’identificadors UUID únics")
        print("3. Consulta de metadades embegudes en PNG")
        print("4. Visualització d’imatges amb metadades")
        print("5. Càrrega i visualització de galeries JSON")
        print("6. Cerca d’imatges segons criteris")
        print("7. Generació de galeries basades en cerques")
        print("8. Imprimir TOTES les metadades de TOTES les imatges")
        print("0. Sortir")

        op = input("Opció: ").strip()

        # --- Func1 ---
        if op == "1":
            img_files.reload_fs(cfg.ROOT_DIR)
            files = sorted(list(img_files._files_curr))
            print(f"\n{len(files)} imatges trobades:\n")
            for f in files:
                print(" -", f)

        # --- Func2 ---
        elif op == "2":
            img_files.reload_fs(cfg.ROOT_DIR)
            print("\nGenerant UUID per a cada arxiu PNG...\n")
            for f in sorted(list(img_files._files_curr)):
                uid = img_ids.generate_uuid(f)
                if uid:
                    img_data.add_image(uid, os.path.join(cfg.ROOT_DIR, f))
                    print(f"{f}  →  {uid}")
            print(f"\nTotal UUID generats: {len(img_ids)}")

        # --- Func3 ---
        elif op == "3":
            uuid = input("Introdueix UUID: ").strip()
            img_data.load_metadata(uuid)
            print("Metadades carregades.")
            print(img_data._data.get(uuid, {}))

        # --- Func4 ---
        elif op == "4":
            uuid = input("UUID: ").strip()
            img_data.load_metadata(uuid)
            img_viewer.show_image(uuid, mode=1)

        # --- Func5 ---
        elif op == "5":
            path = input("Path de la galeria JSON: ").strip()
            gal = Gallery(img_ids, img_viewer)
            gal.load_file(path)
            gal.show()

        # --- Func6 ---
        elif op == "6":
            field = input("Camp (prompt/model/seed/cfg_scale/steps/sampler/date): ").strip()
            sub = input("Text a cercar: ").strip()
            if hasattr(searcher, field):
                results = getattr(searcher, field)(sub)
                print(f"\nResultats ({len(results)} coincidències):")
                for u in results:
                    print(" -", u)
            else:
                print("Camp invàlid.")

        # --- Func7 ---
        elif op == "7":
            field = input("Camp per a la cerca: ").strip()
            sub = input("Text a cercar: ").strip()
            gal_name = input("Nom de la nova galeria: ").strip()

            if hasattr(searcher, field):
                results = getattr(searcher, field)(sub)
                print(f"S'han trobat {len(results)} imatges.")
                gal = Gallery(img_ids, img_viewer)
                for u in results:
                    gal.add_image_at_end(u)
                print(f"Galeria '{gal_name}' creada amb {len(gal)} imatges.")
                gal.show()
            else:
                print("Camp invàlid.")

        # --- NOVA OPCIÓ 8 ---
        elif op == "8":
            print("\n=== METADADES DE TOTES LES IMATGES ===\n")
            if len(img_data._data) == 0:
                print("No hi ha metadades carregades. Primer executa l'opció 2 i després 3.")
            else:
                for uuid in img_data._data:
                    print(f"\n--- UUID: {uuid} ---")
                    img_data.load_metadata(uuid)
                    print(img_data._data.get(uuid, {}))

        elif op == "0":
            print("Sortint...")
            break

        else:
            print("Opció no vàlida.")

if __name__ == "__main__":
    main()


import os
import json
import logging

logger = logging.getLogger(__name__)

def save_to_json(data: dict, base_path: str, endpoint: str, year: int) -> bool:
    """
    Létrehozza a szükséges mappastruktúrát ha még nem létezik és lementi a JSON adatot.
    True-val tér vissza, ha a mentés sikeres volt, egyébként False.
    """
    if not data:
        logger.warning(f"Nincs mentendő adat a következőhöz: {endpoint} - {year}")
        return False

    try:
        folder_path = os.path.join(base_path, endpoint, f"year={year}")
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{year}_{endpoint}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        logger.info(f"Fájl lementve: {file_path}")
        return True

    except OSError as os_err:

        logger.error(f"Fájlrendszer hiba a mentés során a {folder_path} útvonalon: {os_err}")
        return False
    except TypeError as type_err:
        logger.error(f"Adattípus hiba a JSON formázásakor: {type_err}")
        return False
    except Exception as e:
        logger.error(f"Váratlan hiba a mentés során: {str(e)}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
    
    dummy_data = {"test": "Sikeresen működik a storage modul!", "year": 2023}
    
    save_to_json(data=dummy_data, base_path="./test_data", endpoint="test_endpoint", year=2023)
import logging
import time

# Saját modulok importálása
from extractor import fetch_from_api
from storage import save_to_json
from config_loader import load_config  

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("F1_Bronze_Pipeline")

def main():
    logger.info("--- F1 Bronze Pipeline Indítása ---")
    
    # Központosított konfiguráció betöltése
    config = load_config()
    if not config:
        logger.critical("Kritikus hiba a konfiguráció betöltésekor. Leállás.")
        return

    base_url = config["api"]["base_url"]
    limit = config["api"]["limit"]
    timeout = config["api"]["timeout"]
    start_year = config["pipeline"]["start_year"]
    end_year = config["pipeline"]["end_year"]
    endpoints = config["pipeline"]["endpoints"]
    
    # Itt már a specifikus bronze_path-t hívjuk a configból
    base_path = config["storage"]["bronze_path"]

    stats = {"sikeres": 0, "sikertelen": 0}

    for year in range(start_year, end_year + 1):
        for endpoint in endpoints:
            logger.info(f"Feldolgozás alatt: {year} - {endpoint}")
            url = f"{base_url}/{year}/{endpoint}.json?limit={limit}"
            
            data = fetch_from_api(url, timeout=timeout)
            
            if data:
                success = save_to_json(data, base_path, endpoint, year)
                if success:
                    stats["sikeres"] += 1
                else:
                    stats["sikertelen"] += 1
            else:
                stats["sikertelen"] += 1

    logger.info("--- F1 Bronze Pipeline Befejeződött ---")
    logger.info(f"Összegzés: {stats['sikeres']} sikeres mentés, {stats['sikertelen']} hiba.")

if __name__ == "__main__":
    main()
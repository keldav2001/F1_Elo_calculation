import os
import json
import logging
import time

from extractor import fetch_from_api
from storage import save_to_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("F1_Pipeline")

def load_config(config_path="config.json"):
    """Beolvassa a konfigurációt, Docker-barát módon kezelve a környezeti változókat."""
    config = {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            logger.info(f"Sikeresen beolvasva: {config_path}")
    except FileNotFoundError:
        logger.warning(f"A {config_path} nem található, környezeti változókra és alapértékekre támaszkodunk.")
    except json.JSONDecodeError:
        logger.error(f"A {config_path} nem érvényes JSON formátumú!")
        return None


    api = config.get("api", {})
    api["base_url"] = os.getenv("F1_API_URL", api.get("base_url", "https://api.jolpi.ca/ergast/f1"))
    api["limit"] = int(os.getenv("F1_API_LIMIT", api.get("limit", 1000)))
    api["timeout"] = int(os.getenv("F1_API_TIMEOUT", api.get("timeout", 10)))
    config["api"] = api

    pipeline = config.get("pipeline", {})
    pipeline["start_year"] = int(os.getenv("F1_START_YEAR", pipeline.get("start_year", 2000)))
    pipeline["end_year"] = int(os.getenv("F1_END_YEAR", pipeline.get("end_year", 2026)))
  
    pipeline["endpoints"] = pipeline.get("endpoints", ["drivers", "results"])
    config["pipeline"] = pipeline

   
    storage = config.get("storage", {})
    storage["base_path"] = os.getenv("F1_STORAGE_PATH", storage.get("base_path", "../f1data-bronze"))
    config["storage"] = storage

    return config

def main():
    logger.info("--- F1 Data Pipeline Indítása ---")
    
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
    
    base_path = config["storage"]["base_path"]


    stats = {"sikeres": 0, "sikertelen": 0}


    for year in range(start_year, end_year + 1):
        for endpoint in endpoints:
            logger.info(f"Feldolgozás alatt: {year} - {endpoint}")
            
            # URL összeállítása
            # Pl.: https://api.jolpi.ca/ergast/f1/2023/drivers.json?limit=1000
            # Az Ergast API a .json kiterjesztést kéri az URL-ben a formátumhoz
            url = f"{base_url}/{year}/{endpoint}.json?limit={limit}"
            
            # 1. Lépés: Adat kinyerése (Extract)
            data = fetch_from_api(url, timeout=timeout)
            
            if data:
                # 2. Lépés: Adat mentése (Load)
                success = save_to_json(data, base_path, endpoint, year)
                if success:
                    stats["sikeres"] += 1
                else:
                    stats["sikertelen"] += 1
            else:
                stats["sikertelen"] += 1

    logger.info("--- F1 Data Pipeline Befejeződött ---")
    logger.info(f"Összegzés: {stats['sikeres']} sikeres mentés, {stats['sikertelen']} hiba.")

if __name__ == "__main__":
    # Ez indítja el az egész folyamatot
    main()
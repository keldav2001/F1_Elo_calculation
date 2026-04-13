import logging
import time
import os
import glob


# Saját modulok importálása

from config_loader import load_config  

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("F1_Silver_Pipeline")


def main():
    logger.info("--- F1 Bronze Pipeline Indítása ---")
    
    # Központosított konfiguráció betöltése
    config = load_config()
    if not config:
        logger.critical("Kritikus hiba a konfiguráció betöltésekor. Leállás.")
        return

    bronze_path = config["storage"]["bronze_path"]
    silver_path = config["storage"]["silver_path"]
    start_year = config["pipeline"]["start_year"]
    end_year = config["pipeline"]["end_year"]
    endpoints = config["pipeline"]["endpoints"]


if __name__ == "__main__":
    main()
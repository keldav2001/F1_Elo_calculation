import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def load_config(config_path="config.json"):
    config = {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            logger.info(f"Sikeresen beolvasva: {config_path}")
    except FileNotFoundError:

        logger.warning(f"A {config_path} nem található, áttérés a környezeti változókra.")
    except json.JSONDecodeError:
        logger.error(f"A {config_path} nem érvényes JSON formátumú!")
        return None

    pipeline = config.get("pipeline", {})
    pipeline["start_year"] = int(os.getenv("F1_START_YEAR", pipeline.get("start_year", 2000)))
    pipeline["end_year"] = int(os.getenv("F1_END_YEAR", pipeline.get("end_year", 2026)))
    config["pipeline"] = pipeline


    storage = config.get("storage", {})
    storage["base_path"] = os.getenv("F1_STORAGE_PATH", storage.get("base_path", "../f1data-bronze"))
    config["storage"] = storage

    return config


if __name__ == "__main__":
    logger.info("Pipeline inicializálása indítva...")
    config = load_config()
    if config:
        logger.info(f"Kezdő év beállítva: {config['pipeline']['start_year']}")
        logger.info(f"Célmappa beállítva: {config['storage']['base_path']}")
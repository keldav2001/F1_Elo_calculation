import os
import json
import logging

logger = logging.getLogger(__name__)

def load_config(config_path="config.json"):
    """Beolvassa a konfigurációt és kezeli a környezeti változókat."""
    config = {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            logger.debug(f"Sikeresen beolvasva: {config_path}")
    except FileNotFoundError:
        logger.warning(f"A {config_path} nem található, környezeti változókat használunk.")
    except json.JSONDecodeError:
        logger.error(f"A {config_path} nem érvényes JSON!")
        return None

    # API beállítások (csak a Bronze használja, de itt elfér)
    api = config.get("api", {})
    api["base_url"] = os.getenv("F1_API_URL", api.get("base_url", "https://api.jolpi.ca/ergast/f1"))
    api["limit"] = int(os.getenv("F1_API_LIMIT", api.get("limit", 1000)))
    api["timeout"] = int(os.getenv("F1_API_TIMEOUT", api.get("timeout", 10)))
    config["api"] = api

    # Pipeline beállítások (Bronze és Silver is használhatja az éveket)
    pipeline = config.get("pipeline", {})
    pipeline["start_year"] = int(os.getenv("F1_START_YEAR", pipeline.get("start_year", 2000)))
    pipeline["end_year"] = int(os.getenv("F1_END_YEAR", pipeline.get("end_year", 2026)))
    pipeline["endpoints"] = pipeline.get("endpoints", ["drivers", "results"])
    config["pipeline"] = pipeline

    # Storage beállítások (Hol van a Bronze és hova menjen a Silver)
    storage = config.get("storage", {})
    storage["bronze_path"] = os.getenv("F1_BRONZE_PATH", storage.get("bronze_path", "../f1data-bronze"))
    storage["silver_path"] = os.getenv("F1_SILVER_PATH", storage.get("silver_path", "../f1data-silver"))
    config["storage"] = storage

    return config
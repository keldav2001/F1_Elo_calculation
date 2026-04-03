import requests
import logging
import time


logger = logging.getLogger(__name__)

def fetch_from_api(url: str, timeout: int = 10) -> dict:

    logger.info(f"Lekérés indítása: {url}")
    
    try:
        response = requests.get(url, timeout=timeout)
        
        response.raise_for_status()
        
        time.sleep(1)
        
        logger.debug("Lekérés sikeres.")
        return response.json()

    except requests.exceptions.Timeout:
        logger.error(f"Időtúllépés (Timeout) a kérés során: {url}")
        return None
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP hiba történt (státuszkód: {response.status_code}): {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:

        logger.error(f"Hálózati hiba a lekérés során: {req_err}")
        return None


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
    
    test_url = "https://api.jolpi.ca/ergast/f1/2023/drivers.json?limit=10"
    data = fetch_from_api(test_url)
    
    if data:
        print("\nSikeres teszt! Az adat kulcsai:")
        print(data.keys())
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

class RplScraper:

    def _get_driver(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def search(self, country):
        driver = self._get_driver()
        driver.get("https://r.pl/last-minute")
        time.sleep(4)

        search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='kraj']")
        search_input.send_keys(country)
        search_input.submit()
        time.sleep(5)

        offers = driver.find_elements(By.CSS_SELECTOR, "article.offer-card")[:5]

        results = []
        for offer in offers:
            name = offer.find_element(By.CSS_SELECTOR, "h3").text
            price = offer.find_element(By.CSS_SELECTOR, ".price").text
            results.append({"name": name, "price": price})

        driver.quit()
        return results

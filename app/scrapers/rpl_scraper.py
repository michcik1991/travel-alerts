from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def select_country(country_name):
    """
    Funkcja Selenium, która otwiera r.pl/last-minute i zaznacza checkbox
    dla podanego kraju. Zwraca aktywny driver, żeby dalej można było kontynuować scraping.

    :param country_name: nazwa kraju podana przez użytkownika w aplikacji webowej
    :return: driver Selenium
    """
    # --- Konfiguracja Chrome ---
    options = Options()
    # options.add_argument("--headless=new")  # tryb headless jeśli potrzebny
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-popup-blocking")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    # --- Otwieramy stronę ---
    driver.get("https://r.pl/last-minute")
    time.sleep(1)

    # --- Klikamy "Akceptuj wszystkie" cookies ---
    try:
        accept_all_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cmpboxbtnyes"))
        )
        accept_all_button.click()
        print("Kliknięto Akceptuj wszystkie")
    except:
        print("Brak przycisku cookies lub już zaakceptowane")

    # --- Klikamy dropdown "Dokąd" ---
    dropdown_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-test-id='r-input-button:filtyGorne:dokad']")
        )
    )
    try:
        dropdown_button.click()
    except:
        driver.execute_script("arguments[0].click();", dropdown_button)

    # --- Zaznaczamy checkbox dla podanego kraju dynamicznie ---
    country_id_part = country_name.lower()  # np. "oman"
    try:
        checkbox = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//input[contains(@id,':{country_id_part}')]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"Checkbox dla {country_name} zaznaczony")
    except:
        print(f"Nie znaleziono checkboxa dla {country_name}")

    # --- Klikamy przycisk "Wybierz" ---
    try:
        wybierz_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='r-button:filtyGorne:wybierz-dokad']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", wybierz_button)
        time.sleep(0.3)
        try:
            wybierz_button.click()
        except:
            driver.execute_script("arguments[0].click();", wybierz_button)
        print("Kliknięto przycisk Wybierz")
    except:
        print("Nie znaleziono przycisku Wybierz")

    # --- Zwracamy driver, żeby dalej można było kontynuować scraping ---
    return driver

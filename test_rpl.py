from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

def test_rpl():
    # --- Konfiguracja Chrome ---
    options = Options()
    # options.add_argument("--headless=new")  # odkomentuj dla trybu headless
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    # --- 1️⃣ Otwieramy stronę ---
    driver.get("https://r.pl/last-minute")
    time.sleep(1)

    # --- 2️⃣ Klikamy "Akceptuj wszystkie" cookies ---
    try:
        accept_all_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cmpboxbtnyes"))
        )
        accept_all_button.click()
        print("Kliknięto Akceptuj wszystkie")
    except:
        print("Brak przycisku cookies lub już zaakceptowane")

    # --- 3️⃣ Klikamy dropdown "Dokąd" ---
    dropdown_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-test-id='r-input-button:filtyGorne:dokad']")
        )
    )
    try:
        dropdown_button.click()
    except:
        driver.execute_script("arguments[0].click();", dropdown_button)

    # --- 4️⃣ Klikamy checkbox dla Grecji ---
    try:
        checkbox_grecja = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fg-dokad-wyjazd-europa:grecja"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_grecja)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", checkbox_grecja)
        print("Checkbox Grecja zaznaczony")
    except:
        print("Nie znaleziono checkboxa Grecja lub już zaznaczony")

    # --- 5️⃣ Klikamy przycisk "Wybierz" ---
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

    # --- 6️⃣ Czekamy 10 sekund, żeby zobaczyć efekt ---
    print("Czekamy 10 sekund...")
    time.sleep(10)

    driver.quit()
    print("Test zakończony")

if __name__ == "__main__":
    test_rpl()

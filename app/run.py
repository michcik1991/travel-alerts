from flask import Flask, request, render_template
from scrapers.rpl_scraper import select_country  # import z folderu scrapers

app = Flask(__name__)

# Strona startowa z formularzem
@app.route("/")
def index():
    return render_template("index.html")

# Obsługa formularza
@app.route("/search", methods=["POST"])
def search():
    country = request.form.get("country")  # pobieramy kraj z formularza
    if not country:
        return "Nie podano kraju", 400

    # --- Uruchamiamy scraper z wybranym krajem ---
    driver = select_country(country)

    # Na razie tylko uruchamiamy Selenium, nic nie zwracamy oprócz komunikatu
    return f"Zaznaczono {country} w r.pl. Sprawdź przeglądarkę."

if __name__ == "__main__":
    # Uruchomienie aplikacji Flask
    app.run(debug=True)

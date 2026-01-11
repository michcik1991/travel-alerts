from app.scrapers.rpl_scraper import RplScraper
from app.scrapers.itaka_scraper import ItakaScraper

class SearchService:

    def search(self, country):
        results = []
        try:
            results += RplScraper().search(country)
        except Exception as e:
            print(f"R.pl error: {e}")

        try:
            results += ItakaScraper().search(country)
        except Exception as e:
            print(f"Itaka error: {e}")

        return results

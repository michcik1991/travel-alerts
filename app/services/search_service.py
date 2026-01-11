from app.scrapers.rpl_scraper import RplScraper


class SearchService:

    def search(self, country):
        results = []
        try:
            results += RplScraper().search(country)
        except Exception as e:
            print(f"R.pl error: {e}")


        return results

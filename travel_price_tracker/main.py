import time
from partners.savaari_scraper import scrape_savaari

def run_scrapers():
    print("Starting Travel Price Tracker ... \n")

    print(" Scraping Savaari Cab Prices")
    try:
        scrape_savaari()
        print("savaari scraping completed")
    except Exception as e:
        print(f"Error in savaari Scraping:{e}\n")


if __name__ == "__main__":
    start_time = time.time()
    run_scrapers()
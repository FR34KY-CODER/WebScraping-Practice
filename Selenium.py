from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Setup Chrome WebDriver
def setup_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Scrape data from a sample site (example: quotes.toscrape.com)
def scrape_site():
    driver = setup_driver(headless=False)  # Set to True if you want headless
    try:
        url = "https://quotes.toscrape.com/page/1/"
        driver.get(url)

        # Wait for a quote to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quote"))
        )

        # Extract page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        quotes = soup.find_all("div", class_="quote")
        for i, quote in enumerate(quotes):
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            print(f"{i+1}. \"{text}\" - {author}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_site()

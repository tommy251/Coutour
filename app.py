from flask import Flask, jsonify, render_template, send_from_directory
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from chromedriver_autoinstaller import install as install_chromedriver
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for more detail
logger = logging.getLogger(__name__)

install_chromedriver()  # Automatically installs ChromeDriver

# Initialize Flask app
app = Flask(__name__)

# Set up headless Chrome for scraping
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Mimic browser
chrome_options.binary_location = "/usr/bin/google-chrome"  # Specify Chrome binary location for Render

# Categories to scrape from Jumia
categories = {
    "shoes": "https://www.jumia.com.ng/mens-shoes/",
    "clothes": "https://www.jumia.com.ng/mens-clothing/",
    "wristwatches": "https://www.jumia.com.ng/mens-watches/"
}

def scrape_cheapest(category_url):
    driver = None
    try:
        logger.debug(f"Starting scraping for URL: {category_url}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(category_url)
        logger.debug("Page loaded, waiting for products...")

        # Wait for products to load (increased timeout to 60 seconds)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "prd"))
        )
        logger.debug("Products found, parsing HTML...")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("article", class_=["prd", "_fb", "col", "c-prd"])
        logger.debug(f"Found {len(products)} products")

        cheapest_item = None
        min_price = float("inf")

        for product in products:
            try:
                name_elem = product.find("a", class_="core")
                price_elem = product.find("div", class_="prc")
                if name_elem and price_elem:
                    name = name_elem.text.strip()
                    price_text = price_elem.text.strip()
                    price_text = price_text.replace("N", "").replace(",", "").split()[0]
                    price = float(price_text) if price_text and price_text.strip() else float("inf")
                    if price < min_price and price > 0:
                        min_price = price
                        cheapest_item = {"name": name, "price": price, "url": category_url}
            except (AttributeError, ValueError, IndexError) as e:
                logger.error(f"Error parsing product: {e}")
                continue

        return cheapest_item if cheapest_item else {"name": "Not found", "price": 0, "url": category_url}
    except Exception as e:
        logger.error(f"Error scraping {category_url}: {e}")
        return {"name": "Scraping failed", "price": 0, "url": category_url}
    finally:
        if driver:
            driver.quit()

# Serve the index.html file at the root URL
@app.route("/")
def serve_index():
    try:
        logger.debug("Attempting to render index.html")
        return render_template("index.html")  # Changed from cout.html to index.html
    except Exception as e:
        logger.error(f"Failed to render index.html: {e}")
        return "Error rendering template", 500

# Serve static files
@app.route("/static/<path:path>")
def serve_static(path):
    try:
        logger.debug(f"Serving static file: {path}")
        return send_from_directory("static", path)
    except Exception as e:
        logger.error(f"Failed to serve static file {path}: {e}")
        return "Error serving static file", 500

# API endpoint to get the cheapest item in a category
@app.route("/api/cheapest/<category>", methods=["GET"])
def get_cheapest(category):
    logger.debug(f"Received request for category: {category}")
    if category not in categories:
        return jsonify({"error": "Invalid category"}), 400
    
    cheapest_item = scrape_cheapest(categories[category])
    return jsonify(cheapest_item)

if __name__ == "__main__":
    # Only run the development server if this script is executed directly
    app.run(host="0.0.0.0", port=5000, debug=True)
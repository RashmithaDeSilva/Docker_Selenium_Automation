import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_imdb_top_25():
    # 1. Setup Chrome Options
    chrome_options = Options()
    # Important: Run headless implies no UI, but sometimes scraping works better 
    # if you "fake" a real browser user agent.
    # chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 2. Connect to the Remote Browser (the 'chrome' container)
    # The hostname 'chrome' matches the service name in docker-compose.yml
    selenium_host = os.environ.get('SELENIUM_HOST', 'localhost')
    command_executor = f'http://{selenium_host}:4444/wd/hub'
    
    print(f"Connecting to Selenium Grid at {command_executor}...")
    
    driver = webdriver.Remote(
        command_executor=command_executor,
        options=chrome_options
    )

    # Add a delay at the START to let the video recorder catch up
    print("Browser opened. Waiting 3 seconds for video recorder...")
    time.sleep(3)

    try:
        print("Navigating to IMDb Top 250...")
        driver.get("https://www.imdb.com/chart/top/")

        # 3. Wait for the list to load
        wait = WebDriverWait(driver, 10)
        # IMDb's list structure (li elements with class ipc-metadata-list-summary-item)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item")))

        # 4. Find all movie rows
        movie_elements = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")
        
        print(f"\nFound {len(movie_elements)} movies. Extracting top 25...\n")
        print(f"{'RANK':<5} | {'RATING':<6} | {'TITLE'}")
        print("-" * 50)

        # 5. Loop through the first 25 results
        for index, element in enumerate(movie_elements[:25], start=1):
            try:
                # Selectors for Title and Rating (IMDb classes change often, these are current)
                title_element = element.find_element(By.CSS_SELECTOR, "h3.ipc-title__text")
                
                # Try to find rating; sometimes it's missing for unreleased movies, handle gracefully
                try:
                    rating_element = element.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--base")
                    rating = rating_element.text.split()[0] # formatting often returns "9.3 (2.8M)"
                except:
                    rating = "N/A"

                # Clean title (remove "1. " from "1. The Shawshank Redemption")
                title_text = title_element.text
                if title_text[0].isdigit():
                    title_text = title_text.split(" ", 1)[1]

                print(f"{index:<5} | {rating:<6} | {title_text}")

            except Exception as e:
                print(f"Error parsing movie #{index}: {e}")

    finally:
        # Keep the browser open for 5 seconds so the video captures the final state
        print("Waiting 5 seconds to capture final state in video...")
        time.sleep(5)

        # 6. Always quit the driver to release resources
        driver.quit()
        print("\nBrowser session closed.")

if __name__ == "__main__":
    # Small delay to ensure Selenium Grid is fully ready (even with healthcheck)
    time.sleep(2)
    get_imdb_top_25()
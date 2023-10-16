from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc

from selenium import webdriver
import json
import time
import os

cwd = os.getcwd()

# create options with proxy, user agent, and window settings
options = uc.ChromeOptions()
options.add_argument("--disable-gpu")  # Disable GPU acceleration (useful for headless mode)
options.add_argument("--start-maximized")  # Start Chrome maximized
options.add_argument("--no-sandbox")  # Disable sandboxing for headless mode
options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage for headless mode
options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
options.add_argument("--disable-extensions")  # Disable extensions
options.add_argument("--disable-infobars")  # Disable infobars
options.add_argument("--disable-notifications")  # Disable notifications
options.add_argument("--disable-popup-blocking")  # Disable popup blocking
options.add_argument("--disable-translate")  # Disable translation prompts
options.add_argument("--disable-web-security")  # Disable web security
options.add_argument("--disable-logging")  # Disable logging
options.add_argument("--log-level=3")  # Set log level to minimal
options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
options.add_argument("--disable-features=VizDisplayCompositor")  # Disable VizDisplayCompositor
#options.add_argument("--headless")

prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = uc.Chrome(options=options)


# Go to the target URL
driver.get("https://casinoguru-en.com/free-casino-games/slots")

def click_load_more(driver, max_retries):
    retries = 0
    while retries < max_retries:
        try:
            more_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Show More Games')]"))
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", more_button)
            retries += 1
            print(f"Successfully clicked 'Show more' {retries} times.")
            # Scroll down one page
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
        except TimeoutException:
            print("No more 'Show more' button found. Breaking loop.")
            break


# Initialize variables
game_list = []


# Scroll and click the "Load More" button until no more games are loaded
while click_load_more(driver, 700):
    pass

# Parse the page source with BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Find game items and extract information
game_items = soup.find_all('a', class_='game-item-name')
for item in game_items:
    game_name = item.text.strip()
    href = item['href']
    provider_name = item.find('span').text.strip()

    game_list.append({
        'game_name': game_name.split("\n")[0],
        'href': href,
        'provider_name': provider_name,
    })

gamelist_directory = os.path.join(cwd, 'gamelists')
os.makedirs(gamelist_directory, exist_ok=True)

json_file_path = os.path.join(gamelist_directory, f"CasinoGuruRaw.json")
with open(json_file_path, "w") as gamenames_file:
    json.dump(game_list, gamenames_file, indent=4)
    print(f"Game info JSON saved: {json_file_path}")

# Close the WebDriver
driver.quit()
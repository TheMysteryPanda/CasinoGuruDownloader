import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

# Create options with proxy, user agent, and window settings
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
options.add_argument("--headless")

driver = uc.Chrome(options=options)

# Load the JSON file
with open('CasinoGuru-Casinos.json', 'r') as f:
    casinos = json.load(f)

# Navigate to the Casino Review Page and Click the Button
for casino in casinos:
    driver.get(casino["casino_review_link"])
    try:
        # Wait for the button to become clickable
        wait = WebDriverWait(driver, 3)
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cg-tab-main:nth-child(6) > span:nth-child(2)")))
        btn.click()

        # Wait for the payment methods section to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "payment-providers-grid")))

        # Extract Payment Method Data
        payment_methods_div = driver.find_element(By.CLASS_NAME, "payment-providers-grid")
        soup = BeautifulSoup(payment_methods_div.get_attribute('outerHTML'), 'html.parser')

        payment_methods = []
        for span in soup.find_all('span', class_='casino-detail-logos-item'):
            img_tag = span.find('img')
            a_tag = span.find('a')
            if img_tag and a_tag:
                payment_method_name = a_tag.get('title')
                payment_method_image_url = img_tag.get('src')  # Extract the URL from the 'src' attribute of <img>
                payment_methods.append({'name': payment_method_name, 'image_url': payment_method_image_url})

        # Update the payment_methods value
        casino["payment_methods"] = payment_methods
        print(payment_methods)

        # Extract Currencies
        currencies_div = driver.find_element(By.CLASS_NAME, "casino-detail-currencies-body")
        currencies = currencies_div.text.split(',')
        casino["currencies"] = [currency.strip() for currency in currencies]
        print(casino["currencies"])
    except Exception as e:
        print("ERROR FOR THIS CASINO, WE SKIP THAT")

# Quit the WebDriver
driver.quit()

# Save the Updated JSON with Payment Method Data and Currencies
with open('CasinoGuru-Casinos-Payments.json', 'w') as f:
    json.dump(casinos, f, indent=4)

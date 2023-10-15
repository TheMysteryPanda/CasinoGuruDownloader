import json
import requests
from bs4 import BeautifulSoup

# Initialize an empty list to store casino information
casinos_list = []

# Define the base URL and query parameters
base_url = "https://casinoguru-de.com/frontendService/casinoFilterServiceMore"
query_params = {
    "page": 1,
    "initialPage": 1,
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

# Define the tab parameter for the POST request
post_data = {
    "tab": "ALL",
}

# Loop through all 814 pages
for page in range(1, 815):
    query_params["page"] = page

    # Send a POST request to the API
    response = requests.post(base_url, params=query_params, headers=headers, data=post_data)

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all casino card divs
        casino_cards = soup.find_all('div', class_='casino-card')

        # Extract information for each casino card
        for card in casino_cards:
            casino_info = {}
            casino_info['background_color'] = card['style'].split(':')[-1].strip('; ')
            
            # Check if the casino name is available before attempting to extract it
            casino_heading = card.find('div', class_='casino-card-heading')
            if casino_heading and casino_heading.a:
                casino_info['casino_name'] = casino_heading.a.text.strip()
            else:
                casino_info['casino_name'] = "N/A"

            # Extract casino image URLs (wide and square)
            wide_logo = card.find('picture', class_='logo-wide')
            square_logo = card.find('picture', class_='logo-square')
            if wide_logo:
                casino_info['casino_image_src_wide'] = wide_logo.img['src']
            if square_logo:
                casino_info['casino_image_src_square'] = square_logo.img['src']

            # Append the casino info to the list
            casinos_list.append(casino_info)
            print(casino_info)
        print(f"Page {page} scraped.")

# Save the results in casinos.json
with open('casinos.json', 'w', encoding='utf-8') as json_file:
    json.dump(casinos_list, json_file, indent=4, ensure_ascii=False)

print("Scraping complete. Results saved in casinos.json")

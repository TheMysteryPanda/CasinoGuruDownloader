
import json
import requests
from bs4 import BeautifulSoup

# Function to extract the value from the td element
def extract_td_value(td_element):
    bullet_green = td_element.find("span", class_="bullet bullet-green bullet-with-white-svg")
    bullet_grey = td_element.find("span", class_="bullet bullet-grey")
    
    if bullet_green:
        return "True"
    elif bullet_grey:
        return "False"
    else:
        return td_element.get_text(strip=True)

# Initialize an empty list to store game information
game_info_list = []

# Load JSON data from the file
with open('casinoguru.json', 'r') as json_file:
    game_data = json.load(json_file)

# Loop through each game in the JSON data
for game in game_data:
    game_name = game['game_name']
    href = game['href']
    provider_name = game['provider_name']


    # Send a GET request to the game's URL
    response = requests.get(href)

    if response.status_code == 200:
        # Initialize a dictionary to store game information
        game_info = {}

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information from the HTML
        game_background_image = soup.find('div', class_='games-box-placeholder-image').find('img')['src']
        demo_frame_link = soup.find('span', id='game_link')['data-url']
        stats_cards = soup.find_all('div', class_='stats-card-dark')
        game_info_data = soup.find('div', class_='game-detail-main-info')
        game_image_transparent = soup.find('div', class_='game-detail-main-info').find('img')['src']

        # Extract and add the provider image source to the game_info dictionary
        provider_image_source = soup.find('div', class_='provider-img').find('img')['src']
        game_info['Provider Image Source'] = provider_image_source
        
        # Extract and add specific information to the game_info dictionary
        for stats_card in stats_cards:
            label = stats_card.find('label').get_text()
            try:
                value = stats_card.find('b').get_text()
            except AttributeError:
                value = "N/A"  # Set a default value when 'b' element is not found
            game_info[label] = value


        # Extract and add game info to the game_info dictionary
        game_info_items = game_info_data.find_all('tr')
        for item in game_info_items:
            label = item.find('td').get_text(strip=True)
            value_td = item.find_all('td')[1]
            value = extract_td_value(value_td)
            game_info[label] = value

        # Extract and add the game tags to the game_info dictionary
        game_tags = []
        game_tags_container = soup.find('div', class_='game-detail-main-themes-wrapper')
        if game_tags_container:
            game_tags_elements = game_tags_container.find_all('a', class_='game-detail-main-theme')
            for tag_element in game_tags_elements:
                game_tags.append(tag_element.get_text(strip=True))

        game_info['game_name'] = game_name
        game_info['provider_name'] = provider_name

        game_info['Game Tags'] = game_tags
        # Add the game's background image and demo frame link to the game_info dictionary
        game_info['Game Background Image'] = game_background_image
        game_info['Demo Frame Link'] = demo_frame_link

        game_info['game_image_src_transparent'] = game_image_transparent

        # Append the game_info dictionary to the game_info_list
        game_info_list.append(game_info)
        print(game_info)

    else:
        print(f"Failed to fetch data for {game_name}")

# Save the extracted game information to a new JSON file called "Test.json"
with open('Test.json', 'w') as output_json_file:
    json.dump(game_info_list, output_json_file, indent=4)

print("Data saved to Test.json")

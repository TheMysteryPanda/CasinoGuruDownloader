import os
import requests
from urllib.parse import urlparse

# Create the output folder if it doesn't exist
output_folder = "payment_logos"
os.makedirs(output_folder, exist_ok=True)

# Function to extract provider name from URL
def extract_provider_name(url):
    # Split the URL by '/' and get the second-to-last part
    parts = url.split('/')
    if len(parts) >= 1:
        return parts[-1]
    else:
        return "unknown"

# Read URLs from the urls.txt file
with open("urls.txt", "r") as file:
    urls = file.readlines()

for url in urls:
    url = url.strip()
    try:
        # Extract the provider name from the URL
        provider_name = extract_provider_name(url)
        
        # Get the image content
        response = requests.get(url)
        if response.status_code == 200:
            # Get the file extension from the URL
            file_extension = os.path.splitext(urlparse(url).path)[1]
            
            # Save the image to the provider_logos folder with the provider name as the filename
            file_name = os.path.join(output_folder, f"{provider_name}{file_extension}")
            with open(file_name, "wb") as output_file:
                output_file.write(response.content)
            print(f"Downloaded and saved: {file_name}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

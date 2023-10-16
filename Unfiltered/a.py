import os
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
import shutil

# Create the output folder if it doesn't exist
output_folder = "providerlogos_white"
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
        provider_name = extract_provider_name(url).split("?")[0]
        
        # Get the image content
        response = requests.get(url)
        if response.status_code == 200:
            # Check if the image is in SVG format
            if "image/svg+xml" in response.headers.get("content-type", ""):
                # Save the SVG image to the output folder
                svg_file_name = os.path.join(output_folder, f"{provider_name}")
                with open(svg_file_name, "wb") as output_file:
                    output_file.write(response.content)
                print(f"SVG image already exists, copied: {svg_file_name}")
            elif "image/png" in response.headers.get("content-type", ""):
                # Convert the PNG image to SVG
                img = Image.open(BytesIO(response.content))
                svg_file_name = os.path.join(output_folder, f"{provider_name}.svg")
                img.save(svg_file_name)
                print(f"Converted and saved as SVG: {svg_file_name}")
            else:
                print(f"Image is not in PNG or SVG format: {url}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

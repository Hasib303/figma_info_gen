import os
import requests
import json
from PIL import Image
from io import BytesIO

# --- Configuration ---
FIGMA_API_TOKEN = os.environ.get("FIGMA_API_TOKEN")
OUTPUT_DIR = "figma_screenshots"

# --- Helper Functions ---

def get_figma_file_key(url):
    """Extracts the file key from a Figma URL."""
    # https://www.figma.com/file/FILE_KEY/project-name
    # or https://www.figma.com/design/FILE_KEY/project-name
    parts = url.split("/")
    if "file" in parts:
        return parts[parts.index("file") + 1]
    elif "design" in parts:
        return parts[parts.index("design") + 1]
    return None


def get_figma_file(file_key, api_token):
    """Fetches the Figma file data."""
    url = f"https://api.figma.com/v1/files/{file_key}"
    headers = {"X-Figma-Token": api_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def get_node_image(file_key, node_id, api_token):
    """Fetches a rendered image of a specific node."""
    url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png"
    headers = {"X-Figma-Token": api_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    image_url = response.json()["images"][node_id]
    
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    return Image.open(BytesIO(image_response.content))

def main():
    """Main function to run the screenshot process."""
    if not FIGMA_API_TOKEN:
        print("Error: FIGMA_API_TOKEN environment variable not set.")
        return

    figma_url = input("Enter Figma project URL: ")

    file_key = get_figma_file_key(figma_url)
    if not file_key:
        print("Error: Could not extract file key from the provided URL.")
        return

    print(f"Fetching Figma file: {file_key}")
    try:
        figma_data = get_figma_file(file_key, FIGMA_API_TOKEN)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Figma file: {e}")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("Processing pages and nodes...")
    for page in figma_data["document"]["children"]:
        if page["type"] == "CANVAS":
            print(f"  - Processing page: {page['name']}")
            for node in page["children"]:
                node_id = node["id"]
                node_name = node["name"].replace("/", "_").replace("\\", "_")
                output_path = os.path.join(OUTPUT_DIR, f"{page['name']}_{node_name}.png")

                print(f"    - Capturing node: {node_name} ({node_id})")
                try:
                    image = get_node_image(file_key, node_id, FIGMA_API_TOKEN)
                    image.save(output_path)
                    print(f"      - Saved to: {output_path}")
                except requests.exceptions.RequestException as e:
                    print(f"      - Error capturing node {node_id}: {e}")

    print("\nScreenshot process complete.")
    print(f"Screenshots saved in the '{OUTPUT_DIR}' directory.")

if __name__ == "__main__":
    main()

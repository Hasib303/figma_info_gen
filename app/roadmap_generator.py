import os
import base64
import openai
import json

# --- Configuration ---
SCREENSHOTS_DIR = "figma_screenshots"
# LLM_MODEL = "gpt-4"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# --- Helper Functions ---

def encode_image_to_base64(filepath):
    """Encodes an image file to a base64 string."""
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_gpt4(image_path, client):
    print(f"Analyzing image: {os.path.basename(image_path)}...")
    try:
        base64_image = encode_image_to_base64(image_path)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Generate a summary describing the UI components, layout, and potential interactions."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1024,
        )
        summary = response.choices[0].message.content
        return {
            "image": os.path.basename(image_path),
            "description": summary
        }
    except Exception as e:
        print(f"Error analyzing image {os.path.basename(image_path)}: {e}")
        return {
            "image": os.path.basename(image_path),
            "description": "Error during analysis."
        }

def generate_roadmap_with_gpt4(image_analyses, client):
    """Generates a project roadmap from the analysis of all images using GPT-4."""
    print("\nSynthesizing project roadmap...")
    
    prompt_context = "\n".join([f"- Image: {analysis['image']}\n  Description: {analysis['description']}" for analysis in image_analyses])
    
    final_prompt = f"""
    Based on the following analysis of UI screenshots from a Figma project, please generate a comprehensive development task list for frontend, backend, and AI(if any).

    Here are the analyses of the individual screens:
    {prompt_context}

    Please provide a task list in the following structure, :
    1.  Frontend Tasks: List of tasks for frontend development.
    2.  Backend Tasks: List of tasks for backend development.
    3.  AI Tasks: List of tasks for AI development.

    For example, for AI tasks the list will be like this:
    1. Game Outcome Prediction Model

    2. Top Performer Prediction
    For each team, predict top 2 batters & 2 pitchers

    3. Player Position Mapping
    Given team + lineup, assign field positions

    4. Head-to-Head Record Generator

    5. Natural Language Generator
    Turn model outputs into friendly explanations
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo", # Use a text-based model for the final synthesis
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating roadmap: {e}"

def main():
    """Main function to run the roadmap generation process."""
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    if not os.path.exists(SCREENSHOTS_DIR):
        print(f"Error: Directory '{SCREENSHOTS_DIR}' not found.")
        print("Please run the `figma_screenshot.py` script first to download the images.")
        return

    image_files = []
    for root, dirs, files in os.walk(SCREENSHOTS_DIR):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))

    if not image_files:
        print(f"No images found in the '{SCREENSHOTS_DIR}' directory.")
        return

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Step 1: Analyze each image
    all_analyses = []
    for image_file in image_files:
        analysis = analyze_image_with_gpt4(image_file, client)
        all_analyses.append(analysis)

    # Step 2: Generate the roadmap
    roadmap = generate_roadmap_with_gpt4(all_analyses, client)

    # Step 3: Print the final roadmap
    print("\n--- Generated Development Roadmap ---")
    print(roadmap)

    OUTPUT_FILENAME = "roadmap.txt"
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        f.write(roadmap or "")
    
    print(f"\n--- Development Roadmap Generation Complete ---")
    print(f"The roadmap has been saved to: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()
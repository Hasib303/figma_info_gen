import app.figma_screenshot as figma_screenshot
import app.roadmap_generator as roadmap_generator

def main():
    """
    Main function to run the entire process.
    1. Get screenshots from Figma.
    2. Generate a roadmap from the screenshots.
    """
    print("Starting Figma Screenshot Process ---")
    figma_screenshot.main()
    print("\nFigma Screenshot Process Finished ---")

    print("\nStarting Roadmap Generation Process ---")
    roadmap_generator.main()
    print("\nRoadmap Generation Process Finished ---")

if __name__ == "__main__":
    main()

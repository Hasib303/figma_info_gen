# Figma to Roadmap Generator

This project provides a streamlined workflow to analyze a Figma design and generate a comprehensive development roadmap using a multimodal AI model. It uses two main scripts:

1.  `figma_screenshot.py`: Downloads all the frames and layers from your Figma project as PNG images.
2.  `roadmap_generator.py`: Uses a multimodal AI model (like LLaVA via Ollama) to analyze the downloaded images and generate a detailed development roadmap.

## 🚀 Features

-   **Figma API Integration**: Connects to your Figma project to extract and download visual components.
-   **Automated Screenshotting**: Captures every frame and layer, ensuring a complete visual representation of your design.
-   **AI-Powered Vision Analysis**: Leverages a multimodal AI to understand the purpose, components, and user flows of each screenshot.
-   **Roadmap Generation**: Synthesizes the visual analysis into a structured development plan, including a project overview, key features, and technology stack suggestions.

## 📋 Prerequisites

1.  **Python 3.8+**
2.  **Figma API Token**: You can get this from your Figma Account Settings under the "Personal access tokens" section.
3.  **Ollama**: This tool is required to run the local multimodal AI model. You can install it from [ollama.ai](https://ollama.ai).

## 🛠️ Installation & Setup

**Step 1: Clone the Repository**
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

**Step 2: Set Up a Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

**Step 3: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Set Your Figma API Token**

You need to set your Figma API token as an environment variable. For the current terminal session, you can use:

*   **On macOS/Linux:**
    ```bash
    export FIGMA_API_TOKEN="your_figma_api_token_here"
    ```
*   **On Windows:**
    ```bash
    set FIGMA_API_TOKEN="your_figma_api_token_here"
    ```

**Step 5: Download the AI Model**

This project uses a local multimodal model through Ollama. You need to pull the model to your machine. We recommend `llava`.

```bash
ollama pull llava
```

## 🎯 How to Use

The workflow is a simple two-step process.

**Step 1: Take Screenshots of Your Figma Project**

Run the `figma_screenshot.py` script. It will prompt you to enter the URL of your Figma project.

```bash
python figma_screenshot.py
```

This will create a `figma_screenshots` directory and fill it with PNG images of all the frames and layers from your design.

**Step 2: Generate the Development Roadmap**

Once the screenshots are downloaded, run the `roadmap_generator.py` script.

```bash
python roadmap_generator.py
```

This script will:
1.  Analyze each image in the `figma_screenshots` folder using the `llava` model.
2.  Synthesize the findings into a complete project plan.
3.  Save the output to a file named `development_roadmap.txt`.

## 📊 Example Output (`development_roadmap.txt`)

Your output will be a text file containing a detailed plan similar to this:

```text
**Project Overview:**
A mobile application for sports fans that allows them to view team stats, predict game outcomes, and manage their favorite teams.

**Key Features:**
- User Authentication (Login/Sign Up)
- Home screen with team listings and upcoming games.
- Team detail view with player rosters and statistics.
- Game prediction interface.
- User profile section.

**Suggested Technology Stack:**
- **Frontend:** React Native or Flutter for cross-platform mobile development.
- **Backend:** Python (FastAPI or Django) or Node.js (Express) for the API.
- **Database:** PostgreSQL or MongoDB.

**Development Phases:**
1.  **Phase 1: Core UI & User Authentication**
    - Implement the main navigation and screen layouts.
    - Build the login and sign-up flows.
    - Set up the backend API for user management.
2.  **Phase 2: Team and Player Data Integration**
    - Develop API endpoints to serve team and player data.
    - Build the UI to display team lists and player rosters.
3.  **Phase 3: Game Prediction Feature**
    - Create the UI for making game predictions.
    - Implement the backend logic to save and process predictions.
```

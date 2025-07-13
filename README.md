# Figma Project Task Analyzer

Automatically analyze Figma design files and generate structured task lists for frontend, backend, and AI development work.

## Features

- **Frontend Task Identification**: Analyzes UI components, pages, and interactive elements
- **Backend Task Detection**: Identifies data flows, authentication needs, and API requirements  
- **AI Task Recognition**: Detects smart features, search functionality, and ML opportunities
- **Structured Output**: Generates organized task lists with numbered items

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get your Figma API token:
   - Go to Figma → Settings → Security
   - Generate new personal access token
   - Copy the token

3. Set environment variable:
```bash
export FIGMA_API_TOKEN="your_token_here"
```

## Usage

### Command Line
```bash
python figma_analyzer.py
```

### Programmatic Usage
```python
from figma_analyzer import FigmaAnalyzer

analyzer = FigmaAnalyzer(api_token="your_token")
tasks = analyzer.analyze_figma_project("https://figma.com/file/...")
summary = analyzer.generate_summary(tasks)
print(summary)
```

## Output Format

```
# Project Task Analysis Summary

## Frontend Tasks:
Task-1: Create Header component
Task-2: Implement Dashboard page/screen
Task-3: Create form validation for email field

## Backend Tasks:
Task-1: Create API endpoint for user data
Task-2: Implement user authentication system
Task-3: Set up session management

## AI Tasks:
Task-1: Implement search algorithm and indexing
Task-2: Create recommendation engine
Task-3: Add content analysis and tagging
```

## Supported Design Patterns

The analyzer recognizes common design patterns and generates relevant tasks:

- **UI Components**: Buttons, forms, navigation, cards
- **Pages/Screens**: Landing pages, dashboards, profiles
- **Data Features**: Lists, feeds, user-generated content
- **Authentication**: Login/signup flows, user management
- **Smart Features**: Search, recommendations, content generation
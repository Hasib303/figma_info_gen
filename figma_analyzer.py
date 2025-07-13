import requests
import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TaskCategory:
    frontend: List[str]
    backend: List[str] 
    ai: List[str]

class FigmaAnalyzer:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-Figma-Token": api_token,
            "Content-Type": "application/json"
        }
    
    def extract_file_key(self, figma_url: str) -> str:
        """Extract file key from Figma URL"""
        parsed = urlparse(figma_url)
        path_parts = parsed.path.split('/')
        
        # Handle both old format (/file/) and new format (/design/)
        for i, part in enumerate(path_parts):
            if part in ['file', 'design'] and i + 1 < len(path_parts):
                return path_parts[i + 1]
        
        raise ValueError("Invalid Figma URL format")           
    
    def get_file_data(self, file_key: str) -> Dict[str, Any]:
        """Fetch file data from Figma API"""
        url = f"{self.base_url}/files/{file_key}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_project_name(self, file_key: str) -> str:
        """Get the name of the Figma project"""
        file_data = self.get_file_data(file_key)
        project_name = file_data.get('name', 'Unknown Project')
        return project_name
    
    def analyze_components(self, node: Dict[str, Any]) -> List[str]:
        """Analyze UI components to identify frontend tasks"""
        tasks = []
        node_type = node.get('type', '')
        
        # Component-based tasks
        if node_type == 'COMPONENT':
            component_name = node.get('name', 'Unknown Component')
            tasks.append(f"Create {component_name} component")
        
        # Frame/Page analysis
        elif node_type == 'FRAME':
            frame_name = node.get('name', 'Unknown Frame')
            if any(keyword in frame_name.lower() for keyword in ['page', 'screen', 'view']):
                tasks.append(f"Implement {frame_name} page/screen")
        
        # Interactive elements
        if 'children' in node:
            for child in node['children']:
                child_tasks = self.analyze_components(child)
                tasks.extend(child_tasks)
                
                # Button detection
                if child.get('type') == 'RECTANGLE' and 'button' in child.get('name', '').lower():
                    tasks.append(f"Implement {child.get('name', 'button')} functionality")
                
                # Form detection
                if child.get('type') == 'TEXT' and any(keyword in child.get('name', '').lower() 
                    for keyword in ['input', 'field', 'form']):
                    tasks.append(f"Create form validation for {child.get('name', 'field')}")
        
        return tasks
    
    def analyze_data_flows(self, node: Dict[str, Any]) -> List[str]:
        """Analyze design to identify backend requirements"""
        tasks = []
        node_name = node.get('name', '').lower()
        
        # API-related tasks
        if any(keyword in node_name for keyword in ['list', 'feed', 'dashboard', 'profile']):
            tasks.append(f"Create API endpoint for {node.get('name', 'data')}")
            tasks.append(f"Implement database schema for {node.get('name', 'data')}")
        
        # Authentication flows
        if any(keyword in node_name for keyword in ['login', 'signup', 'auth']):
            tasks.append("Implement user authentication system")
            tasks.append("Set up session management")
        
        # Data persistence
        if any(keyword in node_name for keyword in ['form', 'submit', 'save', 'contact us']):
            tasks.append("Create data validation middleware")
            tasks.append("Implement CRUD operations")
        
        # Real-time features
        if any(keyword in node_name for keyword in ['chat', 'notification', 'live']):
            tasks.append("Set up WebSocket connections")
            tasks.append("Implement real-time data synchronization")
        
        if 'children' in node:
            for child in node['children']:
                child_tasks = self.analyze_data_flows(child)
                tasks.extend(child_tasks)
        
        return tasks
    
    def analyze_ai_features(self, node: Dict[str, Any]) -> List[str]:
        """Analyze design to identify AI/ML requirements"""
        tasks = []
        node_name = node.get('name', '').lower()
        
        # Only add tasks if there's a meaningful match (not just partial matches)
        if any(keyword in node_name for keyword in ['chat', 'chatbot', 'messenger']):
            # to avoid false positives
            if len(node_name) >= 3:  
                tasks.append("Implement chatbot functionality")
        
        # Recommendation detection
        if any(keyword in node_name for keyword in ['recommendation', 'suggest', 'suggestions', 'recommend']):
            if len(node_name) > 5:  # Avoid matching very short names
                tasks.append("Implement recommendation engine")

        # Search and discovery detection
        if any(keyword in node_name for keyword in ['search', 'filter', 'find']):
            if len(node_name) > 4:  # Avoid matching very short names
                tasks.append("Implement search algorithm and indexing") 
        
        # Content generation
        if any(keyword in node_name for keyword in ['generate', 'ai', 'smart', 'auto']):
            tasks.append("Integrate AI content generation API")
            tasks.append("Implement content moderation system")
        
        # Image/media processing
        if any(keyword in node_name for keyword in ['upload', 'image', 'photo', 'media']):
            tasks.append("Implement image processing and optimization")
            tasks.append("Add content analysis and tagging")
        
        # Personalization
        if any(keyword in node_name for keyword in ['personalize', 'custom', 'preference']):
            tasks.append("Create user behavior tracking system")
            tasks.append("Implement personalization algorithms")
        
        # Analytics
        if any(keyword in node_name for keyword in ['analytics', 'metrics', 'insights']):
            tasks.append("Set up analytics data pipeline")
            tasks.append("Implement data visualization algorithms")
        
        if 'children' in node:
            for child in node['children']:
                child_tasks = self.analyze_ai_features(child)
                tasks.extend(child_tasks)
        
        return tasks
    
    def analyze_figma_project(self, figma_url: str) -> TaskCategory:
        """Main analysis function"""
        file_key = self.extract_file_key(figma_url)
        file_data = self.get_file_data(file_key)
        
        frontend_tasks = []
        backend_tasks = []
        ai_tasks = []
        
        # Analyze document structure
        document = file_data.get('document', {})
        if 'children' in document:
            for page in document['children']:
                frontend_tasks.extend(self.analyze_components(page))
                backend_tasks.extend(self.analyze_data_flows(page))
                ai_tasks.extend(self.analyze_ai_features(page))
        
        # Remove duplicates while preserving order
        frontend_tasks = list(dict.fromkeys(frontend_tasks))
        backend_tasks = list(dict.fromkeys(backend_tasks))
        ai_tasks = list(dict.fromkeys(ai_tasks))
        
        return TaskCategory(
            frontend=frontend_tasks,
            backend=backend_tasks,
            ai=ai_tasks
        )
    
    def debug_element_names(self, figma_url: str) -> None:
        """Debug function to show all element names in the project"""
        file_key = self.extract_file_key(figma_url)
        file_data = self.get_file_data(file_key)
        
        print("=== DEBUG: All Element Names in Project ===")
        
        def print_element_names(node, level=0):
            indent = "  " * level
            node_type = node.get('type', 'UNKNOWN')
            node_name = node.get('name', 'Unnamed')
            print(f"{indent}{node_type}: {node_name}")
            
            if 'children' in node:
                for child in node['children']:
                    print_element_names(child, level + 1)
        
        document = file_data.get('document', {})
        if 'children' in document:
            for page in document['children']:
                print_element_names(page)
        
        print("=== END DEBUG ===")
    
    def generate_summary(self, tasks: TaskCategory, file_key: str) -> str:
        """Generate formatted summary of tasks"""
        summary = []
        
        # Get project name
        project_name = self.get_project_name(file_key)
        summary.append(f"# Project Task Analysis Summary - {project_name}")
        
        summary.append("## Frontend Tasks:")
        if tasks.frontend:
            for i, task in enumerate(tasks.frontend, 1):
                summary.append(f"Task-{i}: {task}")
        else:
            summary.append("No specific frontend tasks identified")
        
        summary.append("\n## Backend Tasks:")
        if tasks.backend:
            for i, task in enumerate(tasks.backend, 1):
                summary.append(f"Task-{i}: {task}")
        else:
            summary.append("No specific backend tasks identified")
        
        summary.append("\n## AI Tasks:")
        if tasks.ai:
            for i, task in enumerate(tasks.ai, 1):
                summary.append(f"Task-{i}: {task}")
        else:
            summary.append("No specific AI tasks identified")
        
        return "\n".join(summary)

def main():
    """Example usage"""
    # Set your Figma API token
    api_token = os.getenv('FIGMA_API_TOKEN')
    if not api_token:
        print("Please set FIGMA_API_TOKEN environment variable")
        return
    
    # Example Figma URL
    figma_url = input("Enter Figma project URL: ")
    
    try:
        analyzer = FigmaAnalyzer(api_token)
        file_key = analyzer.extract_file_key(figma_url)
        
        # Debug option - uncomment the next line to see all element names
        # analyzer.debug_element_names(figma_url)
        
        tasks = analyzer.analyze_figma_project(figma_url)
        summary = analyzer.generate_summary(tasks, file_key)
        print(summary)
        
        # Save to file
        with open('figma_analysis_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        print("\nSummary saved to figma_analysis_summary.txt")
        
    except Exception as e:
        print(f"Error analyzing Figma project: {e}")

if __name__ == "__main__":
    main()
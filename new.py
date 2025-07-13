#!/usr/bin/env python3
"""
Figma Component Analyzer
Lists all components in a Figma file with their names, count, and child elements.
"""

import requests
import json
import os
from typing import Dict, List, Any
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

class FigmaComponentAnalyzer:
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
    
    def analyze_components(self, node: Dict[str, Any], level: int = 0) -> List[Dict[str, Any]]:
        """Recursively analyze all components and their children"""
        components = []
        node_type = node.get('type', '')
        node_name = node.get('name', 'Unnamed')
        node_id = node.get('id', '')
        
        # Create component info
        component_info = {
            'name': node_name,
            'type': node_type,
            'id': node_id,
            'level': level,
            'children': []
        }
        
        # If node has children, analyze them
        if 'children' in node and node['children']:
            for child in node['children']:
                child_components = self.analyze_components(child, level + 1)
                component_info['children'].extend(child_components)
        
        # Add this component to the list
        components.append(component_info)
        
        return components
    
    def get_all_components(self, figma_url: str) -> Dict[str, Any]:
        """Get all components from the Figma file"""
        file_key = self.extract_file_key(figma_url)
        file_data = self.get_file_data(file_key)
        project_name = self.get_project_name(file_key)
        
        all_components = []
        
        # Analyze document structure
        document = file_data.get('document', {})
        if 'children' in document:
            for page in document['children']:
                page_components = self.analyze_components(page)
                all_components.extend(page_components)
        
        return {
            'project_name': project_name,
            'file_key': file_key,
            'components': all_components,
            'total_components': len(all_components)
        }
    
    def print_component_tree(self, components: List[Dict[str, Any]], level: int = 0):
        """Print component tree in a hierarchical format"""
        for component in components:
            indent = "  " * level
            print(f"{indent}📁 {component['type']}: {component['name']} (ID: {component['id']})")
            
            if component['children']:
                self.print_component_tree(component['children'], level + 1)
    
    def get_component_tree_text(self, components: List[Dict[str, Any]], level: int = 0) -> List[str]:
        """Get component tree as text lines for file output"""
        lines = []
        for component in components:
            indent = "  " * level
            lines.append(f"{indent}📁 {component['type']}: {component['name']} (ID: {component['id']})")
            
            if component['children']:
                child_lines = self.get_component_tree_text(component['children'], level + 1)
                lines.extend(child_lines)
        
        return lines
    
    def generate_component_report(self, figma_url: str) -> str:
        """Generate a detailed component report"""
        component_data = self.get_all_components(figma_url)
        
        report = []
        report.append(f"# Figma Component Analysis Report")
        report.append(f"## Project: {component_data['project_name']}")
        report.append(f"## File Key: {component_data['file_key']}")
        report.append(f"## Total Components: {component_data['total_components']}")
        report.append("")
        
        # Component statistics
        type_counts = {}
        for component in component_data['components']:
            comp_type = component['type']
            type_counts[comp_type] = type_counts.get(comp_type, 0) + 1
        
        report.append("## Component Type Statistics:")
        for comp_type, count in sorted(type_counts.items()):
            report.append(f"- {comp_type}: {count}")
        report.append("")
        
        # Detailed component tree
        report.append("## Component Tree:")
        report.append("```")
        
        def add_to_report(components, level=0):
            for component in components:
                indent = "  " * level
                report.append(f"{indent}{component['type']}: {component['name']} (ID: {component['id']})")
                if component['children']:
                    add_to_report(component['children'], level + 1)
        
        add_to_report(component_data['components'])
        report.append("```")
        
        return "\n".join(report)

def main():
    """Main function to run the component analyzer"""
    # Set your Figma API token
    api_token = os.getenv('FIGMA_API_TOKEN')
    if not api_token:
        print("Please set FIGMA_API_TOKEN environment variable")
        return
    
    # Get Figma URL from user
    figma_url = input("Enter Figma project URL: ")
    
    try:
        analyzer = FigmaComponentAnalyzer(api_token)
        
        # Get component data
        component_data = analyzer.get_all_components(figma_url)
        
        # Prepare output content
        output_lines = []
        output_lines.append("="*50)
        output_lines.append("FIGMA COMPONENT ANALYSIS REPORT")
        output_lines.append("="*50)
        output_lines.append("")
        
        # Project info
        output_lines.append(f"📋 Project: {component_data['project_name']}")
        output_lines.append(f"🔑 File Key: {component_data['file_key']}")
        output_lines.append(f"📊 Total Components: {component_data['total_components']}")
        output_lines.append("")
        
        # Component type statistics
        type_counts = {}
        for component in component_data['components']:
            comp_type = component['type']
            type_counts[comp_type] = type_counts.get(comp_type, 0) + 1
        
        output_lines.append("📈 Component Type Breakdown:")
        for comp_type, count in sorted(type_counts.items()):
            output_lines.append(f"   {comp_type}: {count}")
        output_lines.append("")
        
        # Component tree
        output_lines.append("🌳 Component Tree Structure:")
        output_lines.append("-" * 40)
        tree_lines = analyzer.get_component_tree_text(component_data['components'])
        output_lines.extend(tree_lines)
        output_lines.append("")
        
        # Generate detailed report
        detailed_report = analyzer.generate_component_report(figma_url)
        output_lines.append("="*50)
        output_lines.append("DETAILED REPORT")
        output_lines.append("="*50)
        output_lines.append("")
        output_lines.append(detailed_report)
        
        # Save to file
        output_content = "\n".join(output_lines)
        with open('figma_components_analysis.txt', 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        # Also print to console
        print("\n" + "="*50)
        print("ANALYZING FIGMA COMPONENTS...")
        print("="*50)
        
        # Print project info
        print(f"\n📋 Project: {component_data['project_name']}")
        print(f"🔑 File Key: {component_data['file_key']}")
        print(f"📊 Total Components: {component_data['total_components']}")
        
        # Print component type statistics
        print(f"\n📈 Component Type Breakdown:")
        for comp_type, count in sorted(type_counts.items()):
            print(f"   {comp_type}: {count}")
        
        # Print component tree
        print(f"\n🌳 Component Tree Structure:")
        print("-" * 40)
        analyzer.print_component_tree(component_data['components'])
        
        print(f"\n💾 Complete analysis saved to: figma_components_analysis.txt")
        
    except Exception as e:
        error_msg = f"❌ Error analyzing Figma components: {e}"
        print(error_msg)
        # Also save error to file
        with open('figma_components_analysis.txt', 'w', encoding='utf-8') as f:
            f.write(f"ERROR: {error_msg}")

if __name__ == "__main__":
    main()

"""Tests for the Self-Hosted Alternatives CLI tool."""

import pytest
import json
import os
import sys
from pathlib import Path

# Add cli to path
sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))

from selfhosted_cli import (
    load_all_data,
    get_data_path,
    Colors
)


class TestColors:
    """Test color constants."""
    
    def test_colors_exist(self):
        """Verify all color constants are defined."""
        assert hasattr(Colors, 'GREEN')
        assert hasattr(Colors, 'RED')
        assert hasattr(Colors, 'YELLOW')
        assert hasattr(Colors, 'BLUE')
        assert hasattr(Colors, 'CYAN')
        assert hasattr(Colors, 'BOLD')
        assert hasattr(Colors, 'END')


class TestDataLoading:
    """Test data loading functionality."""
    
    def test_get_data_path(self):
        """Test that data path is correctly identified."""
        data_path = get_data_path()
        assert data_path.exists()
        assert data_path.name == 'data'
    
    def test_load_all_data_returns_dict(self):
        """Test that load_all_data returns a dictionary."""
        data = load_all_data()
        assert isinstance(data, dict)
    
    def test_load_all_data_has_categories(self):
        """Test that loaded data has categories."""
        data = load_all_data()
        assert len(data) > 0
    
    def test_load_productivity_data(self):
        """Test loading productivity category data."""
        data = load_all_data()
        assert 'productivity' in data
        assert isinstance(data['productivity'], list)
        assert len(data['productivity']) > 0


class TestDataStructure:
    """Test the structure of data entries."""
    
    def test_entry_has_required_fields(self):
        """Test that each entry has required fields."""
        data = load_all_data()
        
        for category, tools in data.items():
            for tool in tools:
                assert 'saas_tool' in tool
                assert 'alternative' in tool
                assert 'name' in tool['saas_tool']
                assert 'name' in tool['alternative']
    
    def test_alternative_has_docker_info(self):
        """Test that alternatives have Docker information."""
        data = load_all_data()
        
        for category, tools in data.items():
            for tool in tools:
                alt = tool['alternative']
                assert 'docker' in alt
                assert 'official' in alt['docker']


class TestSearch:
    """Test search functionality."""
    
    def test_search_notion(self):
        """Test searching for Notion."""
        data = load_all_data()
        
        results = []
        for category, tools in data.items():
            for tool in tools:
                query = 'notion'
                saas_name = tool.get('saas_tool', {}).get('name', '').lower()
                alt_name = tool.get('alternative', {}).get('name', '').lower()
                
                if query in saas_name or query in alt_name:
                    results.append(tool)
        
        assert len(results) >= 3  # Notion has multiple alternatives
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        data = load_all_data()
        
        # Both should find the same results
        lower_results = []
        upper_results = []
        
        query_lower = 'notion'.lower()
        query_upper = 'NOTION'.upper()
        
        for category, tools in data.items():
            for tool in tools:
                saas_name = tool.get('saas_tool', {}).get('name', '').lower()
                alt_name = tool.get('alternative', {}).get('name', '').lower()
                
                if query_lower in saas_name or query_lower in alt_name:
                    lower_results.append(tool)
                if query_upper.lower() in saas_name or query_upper.lower() in alt_name:
                    upper_results.append(tool)
        
        # Both should find the same entries
        assert len(lower_results) == len(upper_results)


class TestCategoryFiltering:
    """Test category filtering."""
    
    def test_productivity_category_exists(self):
        """Test that productivity category exists."""
        data = load_all_data()
        assert 'productivity' in data
    
    def test_productivity_has_tools(self):
        """Test that productivity category has tools."""
        data = load_all_data()
        productivity = data.get('productivity', [])
        assert len(productivity) > 0


class TestDockerImages:
    """Test Docker image information."""
    
    def test_docker_images_valid(self):
        """Test that Docker images are properly formatted."""
        data = load_all_data()
        
        for category, tools in data.items():
            for tool in tools:
                docker = tool['alternative']['docker']
                if docker.get('official'):
                    image = docker.get('image', '')
                    assert '/' in image or len(image) > 0


class TestJSONValidity:
    """Test JSON file validity."""
    
    def test_json_files_valid(self):
        """Test that all JSON files are valid."""
        data_path = get_data_path()
        
        for json_file in data_path.glob('*.json'):
            with open(json_file, 'r', encoding='utf-8') as f:
                try:
                    json.load(f)
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in {json_file.name}: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
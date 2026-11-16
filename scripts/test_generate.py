#!/usr/bin/env python3
"""Test script that validates the documentation generation."""

import sys
import json
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate import load_all_data, validate_data, generate_summary


def test_load_all_data():
    """Test that data loads correctly."""
    data = load_all_data()
    
    assert isinstance(data, dict), "Data should be a dictionary"
    assert len(data) > 0, "Data should not be empty"
    
    print(f"[OK] Loaded {len(data)} categories")
    
    for category, tools in data.items():
        assert isinstance(tools, list), f"{category} should be a list"
        assert len(tools) > 0, f"{category} should have entries"
        print(f"  [OK] {category}: {len(tools)} entries")


def test_validate_data():
    """Test data validation."""
    data = load_all_data()
    
    assert validate_data(data), "Validation should pass"
    print("[OK] Validation passed")


def test_generate_summary():
    """Test summary generation."""
    data = load_all_data()
    generate_summary(data)
    
    summary_path = Path(__file__).parent.parent / "data" / "SUMMARY.json"
    
    assert summary_path.exists(), "Summary file should exist"
    
    with open(summary_path) as f:
        summary = json.load(f)
    
    assert 'total_entries' in summary
    assert 'categories' in summary
    
    print(f"[OK] Generated summary: {summary['total_entries']} entries in {len(summary['categories'])} categories")


def test_markdown_files():
    """Test that markdown files were generated."""
    docs_path = Path(__file__).parent.parent / "docs"
    
    assert docs_path.exists(), "Docs directory should exist"
    
    # Check index exists
    index_path = docs_path / "index.md"
    assert index_path.exists(), "Index.md should exist"
    
    # Check category files
    data_path = Path(__file__).parent.parent / "data"
    for json_file in data_path.glob("*.json"):
        category = json_file.stem
        # Skip SUMMARY file
        if category == "SUMMARY":
            continue
        md_file = docs_path / f"{category}.md"
        assert md_file.exists(), f"{category}.md should exist"
    
    print("[OK] All markdown files generated")


def main():
    """Run all tests."""
    print("Running generation tests...\n")
    
    try:
        test_load_all_data()
        test_validate_data()
        test_generate_summary()
        test_markdown_files()
        
        print("\n[OK] All tests passed!")
        return 0
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
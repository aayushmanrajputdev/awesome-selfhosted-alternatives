#!/usr/bin/env python3
"""
Generate documentation and CLI tool for awesome-selfhosted-alternatives.

This script processes the data files and generates:
- Updated markdown documentation
- CLI tool files
- Search indices
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_data_path() -> Path:
    """Get the path to the data directory."""
    return get_project_root() / "data"


def load_all_data() -> Dict[str, List[Dict]]:
    """Load all JSON data files from the data directory."""
    data_path = get_data_path()
    all_data = {}
    
    for json_file in sorted(data_path.glob("*.json")):
        category = json_file.stem
        # Skip SUMMARY file
        if category == "SUMMARY":
            continue
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                all_data[category] = data if isinstance(data, list) else [data]
            except json.JSONDecodeError as e:
                print(f"Error loading {json_file.name}: {e}", file=sys.stderr)
    
    return all_data


def generate_markdown_table(tools: List[Dict]) -> str:
    """Generate a markdown table from tools list."""
    rows = []
    for tool in tools:
        saas = tool.get('saas_tool', {})
        alt = tool.get('alternative', {})
        
        docker_img = alt.get('docker', {}).get('image', 'N/A')
        docker_tag = alt.get('docker', {}).get('tags', [])
        docker_str = f"✅ {docker_img}" if alt.get('docker', {}).get('official') else "❌"
        
        rows.append([
            f"[{saas.get('name', 'Unknown')}]({saas.get('url', '#')})",
            f"[{alt.get('name', 'Unknown')}]({alt.get('url', '#')})",
            alt.get('license', 'Unknown'),
            docker_str,
            tool.get('added_date', 'N/A')
        ])
    
    table = "| SaaS Tool | Alternative | License | Docker | Added |\n"
    table += "|-----------|-------------|---------|--------|-------|\n"
    for row in rows:
        table += "|" + "|".join(str(cell) for cell in row) + "|\n"
    
    return table


def generate_category_pages(all_data: Dict[str, List[Dict]]) -> None:
    """Generate individual markdown pages for each category."""
    docs_path = get_project_root() / "docs"
    
    for category, tools in all_data.items():
        output_file = docs_path / f"{category}.md"
        
        # Generate table of contents
        toc = f"# {category.title().replace('-', ' ').title()} Tools\n\n"
        toc += "Alternatives to popular SaaS tools in this category.\n\n"
        toc += "## Table of Contents\n\n"
        toc += "[Back to Catalog](index.md)\n\n"
        toc += "---\n\n"
        
        # Generate table
        toc += generate_markdown_table(tools)
        
        # Add footer
        toc += f"\n\n---\n\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n"
        toc += f"*{len(tools)} entries in this category*\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(toc)


def generate_index_page(all_data: Dict[str, List[Dict]]) -> None:
    """Generate the main index page."""
    docs_path = get_project_root() / "docs"
    output_file = docs_path / "index.md"
    
    total_tools = sum(len(tools) for tools in all_data.values())
    
    content = f"""# 📚 Self-Hosted Alternatives Catalog

Welcome to the definitive directory of self-hosted alternatives to popular SaaS tools.

## 📊 Quick Stats

- **{total_tools}** total entries
- **{len(all_data)}** categories
- **Growing daily** with community contributions

## 📂 Browse by Category

"""
    
    for category in sorted(all_data.keys()):
        tools_count = len(all_data[category])
        content += f"- [{category.replace('-', ' ').title()}](./{category}.md) ({tools_count} tools)\n"
    
    content += """
## 🚀 Using the CLI

```bash
# Install
pip install -e .

# Search for alternatives
selfhosted search "notion"

# List all tools in a category
selfhosted list --category productivity

# Add a new tool
selfhosted add "Toggl" --alternative "ActivityWatch"
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

*This catalog is maintained by the community. Star the repository to support it! ⭐*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)


def generate_summary(all_data: Dict[str, List[Dict]]) -> None:
    """Generate a summary of all data."""
    summary = {
        'generated_at': datetime.now().isoformat(),
        'categories': list(all_data.keys()),
        'total_entries': sum(len(tools) for tools in all_data.values()),
        'entries_per_category': {
            category: len(tools) 
            for category, tools in all_data.items()
        }
    }
    
    output_file = get_project_root() / "data" / "SUMMARY.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary written to {output_file}")


def validate_data(all_data: Dict[str, List[Dict]]) -> bool:
    """Validate the loaded data."""
    errors = []
    
    for category, tools in all_data.items():
        for i, tool in enumerate(tools):
            if 'saas_tool' not in tool:
                errors.append(f"{category}[{i}]: Missing 'saas_tool'")
            if 'alternative' not in tool:
                errors.append(f"{category}[{i}]: Missing 'alternative'")
            
            saas = tool.get('saas_tool', {})
            alt = tool.get('alternative', {})
            
            if 'name' not in saas:
                errors.append(f"{category}[{i}]: Missing 'saas_tool.name'")
            if 'name' not in alt:
                errors.append(f"{category}[{i}]: Missing 'alternative.name'")
    
    if errors:
        for error in errors:
            print(f"Validation error: {error}", file=sys.stderr)
        return False
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate documentation and CLI tool for awesome-selfhosted-alternatives'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate data before generating'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Generate summary file'
    )
    parser.add_argument(
        '--categories',
        action='store_true',
        help='Generate category pages'
    )
    
    args = parser.parse_args()
    
    # Default: generate everything
    if not (args.validate or args.summary or args.categories):
        args.validate = True
        args.summary = True
        args.categories = True
    
    # Load data
    all_data = load_all_data()
    
    if not all_data:
        print("No data files found!", file=sys.stderr)
        sys.exit(1)
    
    # Validate
    if args.validate:
        print("Validating data...")
        if not validate_data(all_data):
            print("Validation failed!", file=sys.stderr)
            sys.exit(1)
        print("[OK] Validation passed")
    
    # Generate summary
    if args.summary:
        generate_summary(all_data)
    
    # Generate category pages
    if args.categories:
        generate_index_page(all_data)
        generate_category_pages(all_data)
        print(f"[OK] Generated {len(all_data)} category pages")
    
    print(f"\n[OK] Successfully processed {len(all_data)} categories")


if __name__ == '__main__':
    main()
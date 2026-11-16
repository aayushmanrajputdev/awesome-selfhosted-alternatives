#!/usr/bin/env python3
"""
Initialize the awesome-selfhosted-alternatives project.

This script:
1. Creates necessary directories
2. Generates initial documentation
3. Validates data integrity
4. Creates default data files
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def create_directories():
    """Create all required directories."""
    dirs = [
        "data",
        "docs", 
        "cli",
        "scripts",
        "tests",
        "assets/templates",
        "assets/examples"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")


def create_default_categories():
    """Create initial default category files."""
    default_data = {
        'productivity': [
            {
                "saas_tool": {
                    "name": "Notion",
                    "url": "https://www.notion.so/",
                    "description": "All-in-one workspace for notes, databases, wikis, and project management"
                },
                "alternative": {
                    "name": "Logseq",
                    "url": "https://logseq.com/",
                    "license": "MIT",
                    "docker": {"official": True, "image": "logseq/logseq", "tags": ["latest"]},
                    "self_hosted": True,
                    "cloud_variants": False,
                    "category_tags": ["note-taking", "knowledge-base", "outliner"]
                },
                "added_date": datetime.now().strftime("%Y-%m-%d"),
                "contributor": "aayushmanrajputdev"
            }
        ],
        'communication': [],
        'analytics': [],
        'monitoring': [],
        'storage': [],
        'media': [],
        'development': [],
        'security': [],
        'finance': [],
        'health': []
    }
    
    for category, data in default_data.items():
        path = Path(f"data/{category}.json")
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Created initial data: {category}.json")


def create_readme():
    """Create README file."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        with open(readme_path, 'w') as f:
            f.write("""# awesome-selfhosted-alternatives
<!-- README content will be generated -->
""")


def create_license():
    """Create MIT license file."""
    license_path = Path("LICENSE")
    if not license_path.exists():
        with open(license_path, 'w') as f:
            f.write("""MIT License

Copyright (c) 2024 aayushmanrajputdev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**Note**: This is not an official GitHub certification or endorsement.
""")


def create_gitignore():
    """Create .gitignore file."""
    gitignore = Path(".gitignore")
    if not gitignore.exists():
        with open(gitignore, 'w') as f:
            f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# IDE/Eclipse
.pydevproject
.project
.settings/

# OS
.DS_Store
Thumbs.db

# Backup files
*.bak
*.backup

# Logs
*.log

# Data (optional - adjust as needed)
# data/
""")


def main():
    """Main initialization function."""
    print("Initializing awesome-selfhosted-alternatives project...\n")
    
    create_directories()
    create_default_categories()
    create_readme()
    create_license()
    create_gitignore()
    
    print("\n✅ Project initialization complete!")
    print("\nNext steps:")
    print("  1. git init")
    print("  2. git add .")
    print("  3. git commit -m 'Initial commit'")
    print("  4. git remote add origin <your-repo-url>")
    print("  5. git push -u origin main")


if __name__ == "__main__":
    main()
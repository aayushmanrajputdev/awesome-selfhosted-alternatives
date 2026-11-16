# 📖 Documentation

Complete documentation for the Self-Hosted Alternatives ecosystem.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Adding New Alternatives](#adding-new-alternatives)
4. [Docker Deployments](#docker-deployments)
5. [API Reference](#api-reference)
6. [CLI Reference](#cli-reference)

---

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/aayushmanrajputdev/awesome-selfhosted-alternatives.git
cd awesome-selfhosted-alternatives

# Install CLI tools (optional)
pip install -e .
```

### Quick Usage

```bash
# View the catalog
selfhosted list

# Search for alternatives
selfhosted search "notion"

# Add a new tool
selfhosted add "Toggl" --alternative "ActivityWatch"
```

---

## Project Structure

```
awesome-selfhosted-alternatives/
├── data/                      # Core JSON database
│   ├── productivity.json      # Productivity tools
│   ├── communication.json     # Communication tools
│   ├── analytics.json         # Analytics tools
│   └── ... (25+ categories)
├── docs/                      # Documentation
│   ├── index.md              # Catalog index
│   ├── quickstart.md         # Getting started guide
│   └── documentation.md      # This file
├── cli/                       # CLI tool
│   └── selfhosted_cli.py     # Main CLI module
├── scripts/                   # Utility scripts
│   ├── generate.py           # Documentation generator
│   └── pretty_print.py       # Output formatting
├── tests/                     # Test suite
│   └── test_cli.py           # CLI tests
└── assets/                    # Screenshots, logos
    └── templates/              # README templates
```

---

## Adding New Alternatives

### JSON Schema

Every alternative entry follows this structure:

```json
{
  "saas_tool": {
    "name": "Tool Name",
    "url": "https://example.com",
    "description": "Brief description"
  },
  "alternative": {
    "name": "Alternative Name",
    "url": "https://alternative.com",
    "license": "MIT",
    "docker": {
      "official": true,
      "image": "namespace/image",
      "tags": ["latest"]
    },
    "self_hosted": true,
    "cloud_variants": false,
    "category_tags": ["tag1", "tag2"],
    "key_features": ["Feature 1", "Feature 2"]
  },
  "added_date": "2024-01-15",
  "contributor": "username"
}
```

### Adding Manually

Edit `data/<category>.json` and add a new entry:

```json
{
  "saas_tool": {
    "name": "My SaaS",
    "url": "https://saas.com"
  },
  "alternative": {
    "name": "Open Source Clone",
    "url": "https://clone.com",
    "license": "MIT",
    "docker": {
      "official": true,
      "image": "clone/clone",
      "tags": ["latest"]
    }
  },
  "added_date": "2024-01-15",
  "contributor": "your-username"
}
```

---

## Docker Deployments

### Standard Docker Compose

```yaml
version: '3.8'
services:
  app:
    image: organization/app:latest
    ports:
      - "8080:80"
    volumes:
      - ./data:/data
    restart: unless-stopped
```

### Production with HTTPS

```yaml
version: '3.8'
services:
  caddy:
    image: caddy:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data

  app:
    image: organization/app:latest
    restart: unless-stopped

volumes:
  caddy_data:
```

---

## API Reference

The catalog serves data from JSON files, but you can extend it:

### Reading Data

```python
from cli.selfhosted_cli import load_all_data

data = load_all_data()
# Returns: {'productivity': [...], 'communication': [...], ...}
```

### Search Function

```python
def search_tools(query: str, category: str = None) -> List[Dict]:
    """Search for tools matching the query."""
    data = load_all_data()
    results = []
    
    for cat, tools in data.items():
        if category and cat != category:
            continue
        for tool in tools:
            if query.lower() in tool['saas_tool']['name'].lower():
                results.append(tool)
    
    return results
```

---

## CLI Reference

### Commands

| Command | Description |
|---------|-------------|
| `search <query>` | Search for SaaS tools and alternatives |
| `list` | List all tools in a category |
| `add <name>` | Add a new tool to the catalog |
| `verify <tool>` | Verify a tool entry |
| `backup` | Create data backup |
| `stats` | Show catalog statistics |

### Options

- `--category, -c` - Filter by category
- `--format, -f` - Output format (table, csv, json)
- `--license, -l` - License for new tools

### Examples

```bash
# Basic search
selfhosted search notion

# Search by category
selfhosted search "notion" --category productivity

# List all productivity tools as CSV
selfhosted list --category productivity --format csv

# Add a new tool
selfhosted add "Toggl" \
  --saas-url "https://toggl.com" \
  --alternative "ActivityWatch" \
  --alt-url "https://activitywatch.net" \
  --category productivity
```

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License © 2024 aayushmanrajputdev

**Note:** This is not an official GitHub certification or endorsement.
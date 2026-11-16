# 🏗️ Architecture

This document describes the architecture and data flow of the **awesome-selfhosted-alternatives** project.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    awesome-selfhosted-alternatives               │
│                                                                  │
│  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐  │
│  │ Data Files  │────│  Generator   │─────│ Markdown Docs   │  │
│  │   (JSON)    │     │   Script     │     │   (.md)         │  │
│  └─────────────┘     └──────────────┘     └─────────────────┘  │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐  │
│  │   CLI Tool  │────│   Output     │─────│    Tables       │  │
│  │   (Python)  │     │   Formats    │     │   (CSV,JSON)    │  │
│  └─────────────┘     └──────────────┘     └─────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
                    ┌─────────────────┐
                    │   data/*.json   │
                    │  (Source of      │
                    │   Truth)         │
                    └────────┬────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────┐
│              scripts/generate.py                │
│  - Loads all JSON files                         │
│  - Validates data structure                     │
│  - Generates markdown pages                     │
│  - Creates SUMMARY.json                         │
└─────────────────────────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ docs/    │     │ README.md │     │ data/    │
    │ index.md │     │ (Updated) │     │ SUMMARY  │
    │ *.md     │     │           │     │ .json    │
    └──────────┘     └──────────┘     └──────────┘
```

## File Structure

```
awesome-selfhosted-alternatives/
├── data/                      # Core JSON database (Source of Truth)
│   ├── productivity.json      # Productivity tools
│   ├── communication.json     # Communication tools
│   ├── analytics.json         # Analytics tools
│   ├── monitoring.json        # Monitoring tools
│   ├── storage.json           # File storage tools
│   ├── media.json             # Media tools
│   ├── development.json       # Development tools
│   ├── security.json          # Security tools
│   ├── finance.json           # Financial tools
│   ├── health.json            # Health/Medical tools
│   └── SUMMARY.json           # Auto-generated summary
│
├── cli/                       # CLI tool implementation
│   └── selfhosted_cli.py      # Main CLI module
│
├── scripts/                   # Utility scripts
│   ├── generate.py            # Documentation generator
│   ├── test_generate.py       # Test suite
│   ├── init.py                # Project initialization
│   └── list_categories.py     # Category listing utility
│
├── docs/                      # Generated documentation
│   ├── index.md               # Catalog index
│   ├── quickstart.md          # Getting started guide
│   ├── documentation.md       # Full docs
│   ├── ARCHITECTURE.md        # This file
│   └── <category>.md          # Generated category pages
│
├── tests/                     # Test files
│   └── test_cli.py            # CLI unit tests
│
├── assets/                    # Static assets
│   └── templates/             # README & CONTRIBUTING templates
│
├── setup.py                   # Package setup
├── pyproject.toml             # Project configuration
├── README.md                  # Main entry point
├── CONTRIBUTING.md            # Contribution guidelines
└── LICENSE                      # MIT License
```

## Data Schema

### Entry Structure

```json
{
  "saas_tool": {
    "name": "Notion",
    "url": "https://www.notion.so/",
    "description": "All-in-one workspace"
  },
  "alternative": {
    "name": "Logseq",
    "url": "https://logseq.com/",
    "license": "MIT",
    "docker": {
      "official": true,
      "image": "logseq/logseq",
      "tags": ["latest", "stable"]
    },
    "self_hosted": true,
    "cloud_variants": false,
    "category_tags": ["note-taking", "knowledge-base"],
    "key_features": ["Feature 1", "Feature 2"]
  },
  "added_date": "2024-01-15",
  "contributor": "username",
  "confidence": "high"
}
```

## CLI Architecture

```
selfhosted CLI
    │
    ├── search <query>
    │   └── Filters by: saas_tool.name, alternative.name, description
    │
    ├── list [--category C]
    │   └── Outputs: Table, CSV, or JSON
    │
    ├── add <name> --alternative <alt>
    │   └── Creates new entry in data/<category>.json
    │
    ├── verify <tool>
    │   └── Checks entry integrity and completeness
    │
    └── stats
        └── Shows catalog statistics
```

### Command Processing Flow

```
User Input
    │
    ▼
┌─────────────────┐
│  argparse       │ Parse arguments
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Command Router │ Map to handler
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Handler Func   │ Process request
│  (cmd_search,   │
│   cmd_list, etc)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Loading   │ Load JSON files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Output         │ Format and print
│  (tabulate,     │ results
│   csv, etc)     │
└─────────────────┘
```

## Generation Pipeline

```
                    ┌─────────────────┐
                    │   data/*.json   │
                    └────────┬────────┘
                             │
                             ▼
              ┌─────────────────────────┐
              │   scripts/generate.py    │
              └──────────┬──────────────┘
                           │
        ┌────────┬─────────┼─────────┬────────┐
        │        │         │         │        │
        ▼        ▼         ▼         ▼        ▼
   ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
   │ index │ │ .md   │ │ data/ │ │ docs/ │ │ tests │
   │ .md   │ │       │ │ stats │ │ .md   │ │ .py   │
   └───────┘ └───────┘ └───────┘ └───────┘ └───────┘
```

## Extension Points

### Adding New Categories

1. Create `data/<new-category>.json`
2. Add entries using the schema above
3. Run `python scripts/generate.py` to generate docs

### Adding New CLI Commands

1. Create a new command handler function
2. Add it to the subparsers in `create_parser()`
3. Add the entry to the `commands` dictionary

### Adding New Output Formats

1. Create a new formatter function
2. Add format option to relevant commands
3. Handle output in the command handler

## Performance Considerations

- **Data Loading**: JSON files are small (<100KB each), so fast to load
- **CLI**: Sub-second response times for all commands
- **Search**: Linear scan through categories (acceptable for <10K entries)
- **Generation**: One-time operation, <1 second for full regeneration

## Future Improvements

1. **Database Backend**: Move to SQLite/PostgreSQL for larger scale
2. **Full-text Search**: Add Elasticsearch/Solr integration
3. **API Layer**: RESTful API for web frontend
4. **User Ratings**: Allow community voting on alternatives
5. **Compatibility Matrix**: OS/platform support indicators
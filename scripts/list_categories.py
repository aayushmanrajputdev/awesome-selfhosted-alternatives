#!/usr/bin/env python3
"""List all available categories and their tool counts."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.selfhosted_cli import load_all_data


def main():
    """Display categories and counts."""
    data = load_all_data()
    
    print(f"\n{'Category':<30} {'Tools':>10}")
    print("-" * 42)
    
    for category in sorted(data.keys()):
        count = len(data[category])
        print(f"{category:<30} {count:>10}")
    
    total = sum(len(tools) for tools in data.values())
    print("-" * 42)
    print(f"{'TOTAL':<30} {total:>10}")


if __name__ == "__main__":
    main()
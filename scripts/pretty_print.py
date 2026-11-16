#!/usr/bin/env python3
"""Pretty print helper functions for CLI output."""

from typing import List, Any


def print_header(text: str, char: str = "=") -> str:
    """Print a formatted header."""
    line = char * len(text)
    return f"\n{line}\n{text}\n{line}\n"


def print_table(headers: List[str], rows: List[List[Any]], align: str = "left") -> str:
    """Print a formatted table."""
    # Calculate column widths
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Build table
    lines = []
    
    # Header
    header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    separator = "-|-".join("-" * w for w in widths)
    
    lines.append(header_line)
    lines.append(separator)
    
    # Rows
    for row in rows:
        row_line = " | ".join(str(cell).ljust(w) for cell, w in zip(row, widths))
        lines.append(row_line)
    
    return "\n".join(lines)


def print_bullet_list(items: List[str], numbered: bool = False) -> str:
    """Print a bullet list."""
    prefix = "%d." if numbered else "- "
    if numbered:
        return "\n".join(f"{prefix % (i+1)} {item}" for i, item in enumerate(items))
    return "\n".join(f"- {item}" for item in items)


def print_quoted(text: str, quote: str = ">") -> str:
    """Print quoted text."""
    lines = text.split('\n')
    return '\n'.join(f"{quote} {line}" for line in lines)


if __name__ == "__main__":
    # Demo usage
    print(print_header("Self-Hosted Alternatives"))
    print(print_table(
        headers=["SaaS Tool", "Alternative", "License"],
        rows=[
            ["Notion", "Logseq", "MIT"],
            ["Todoist", "Wekan", "MIT"],
            ["Grammarly", "LanguageTool", "LGPL-2.1"],
        ]
    ))
    print("\n" + print_bullet_list(["Feature 1", "Feature 2", "Feature 3"]))
    print("\n" + print_quoted("This is a quote"))
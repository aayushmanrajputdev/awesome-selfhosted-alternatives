#!/usr/bin/env python3
"""
Self-Hosted Alternatives CLI Tool

A command-line interface for browsing, searching, and contributing to
the awesome-selfhosted-alternatives directory.

Usage:
    selfhosted search "notion"
    selfhosted add "Toggl" --alternative "ActivityWatch"
    selfhosted list --category productivity
    selfhosted verify "logseq"
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime
from tabulate import tabulate


class Colors:
    """Terminal colors for pretty output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def get_data_path() -> Path:
    """Get the path to the data directory."""
    return Path(__file__).parent.parent / "data"


def load_all_data() -> Dict[str, List[Dict]]:
    """Load all JSON data files from the data directory."""
    data_path = get_data_path()
    all_data = {}
    
    for json_file in data_path.glob("*.json"):
        category = json_file.stem
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                all_data[category] = data if isinstance(data, list) else [data]
            except json.JSONDecodeError:
                print(f"{Colors.RED}Error loading {json_file.name}{Colors.END}")
                continue
    
    return all_data


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗ {message}{Colors.END}", file=sys.stderr)


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")


def cmd_search(args: argparse.Namespace) -> None:
    """Search for SaaS tools and their alternatives."""
    query = args.query.lower()
    all_data = load_all_data()
    
    results = []
    
    for category, tools in all_data.items():
        for tool in tools:
            saas_name = tool.get('saas_tool', {}).get('name', '').lower()
            alt_name = tool.get('alternative', {}).get('name', '').lower()
            
            if query in saas_name or query in alt_name or query in tool.get('description', '').lower():
                saas = tool.get('saas_tool', {})
                alt = tool.get('alternative', {})
                
                results.append({
                    'SaaS Tool': saas.get('name', 'Unknown'),
                    'Alternative': alt.get('name', 'Unknown'),
                    'Category': category.replace('-', ' ').title(),
                    'Docker': '✅' if alt.get('docker', {}).get('official') else '❌',
                    'License': alt.get('license', 'Unknown')
                })
    
    if not results:
        print_warning(f"No results found for '{args.query}'")
        return
    
    print(f"\n{Colors.BOLD}Search Results for '{args.query}':{Colors.END}\n")
    print(tabulate(results, headers='keys', tablefmt='github'))


def cmd_list(args: argparse.Namespace) -> None:
    """List all tools in a category or all tools."""
    all_data = load_all_data()
    
    if args.category:
        category = args.category.lower().replace('_', '-')
        if category not in all_data:
            print_error(f"Category '{args.category}' not found")
            print_info(f"Available categories: {', '.join(sorted(all_data.keys()))}")
            return
        
        tools = all_data[category]
        print(f"\n{Colors.BOLD}{category.title()} Tools ({len(tools)} entries){Colors.END}\n")
    else:
        tools = []
        for category, category_tools in all_data.items():
            tools.extend(category_tools)
    
    table_data = []
    for tool in tools:
        saas = tool.get('saas_tool', {})
        alt = tool.get('alternative', {})
        
        table_data.append({
            'SaaS': saas.get('name', 'Unknown'),
            'Alternative': alt.get('name', 'Unknown'),
            'License': alt.get('license', 'Unknown'),
            'Docker': '✅' if alt.get('docker', {}).get('official') else '❌'
        })
    
    if not table_data:
        print_warning("No tools found")
        return
    
    if args.format == 'csv':
        import csv
        writer = csv.DictWriter(sys.stdout, fieldnames=table_data[0].keys())
        writer.writeheader()
        writer.writerows(table_data)
    else:
        print(tabulate(table_data, headers='keys', tablefmt='github'))


def cmd_add(args: argparse.Namespace) -> None:
    """Add a new SaaS tool and its alternative."""
    if not args.saas or not args.alternative:
        print_error("Both --saas and --alternative must be provided")
        return
    
    data_path = get_data_path()
    category = args.category or 'general'
    
    # Create category file if it doesn't exist
    category_file = data_path / f"{category}.json"
    if not category_file.exists():
        with open(category_file, 'w') as f:
            json.dump([], f)
    
    # Load existing data
    with open(category_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if already exists
    for entry in data:
        if entry.get('saas_tool', {}).get('name', '').lower() == args.saas.lower():
            print_warning(f"'{args.saas}' already exists in {category}")
            return
    
    # Add new entry
    new_entry = {
        'saas_tool': {
            'name': args.saas,
            'url': args.saas_url or '',
            'description': args.description or ''
        },
        'alternative': {
            'name': args.alternative,
            'url': args.alt_url or '',
            'license': args.license or 'MIT',
            'docker': {
                'official': not args.no_docker,
                'image': args.docker_image or '',
                'tags': [args.docker_tag] if args.docker_tag else []
            },
            'self_hosted': not args.cloud_only
        },
        'added_date': datetime.now().strftime('%Y-%m-%d'),
        'contributor': args.contributor or os.environ.get('USER', 'anonymous')
    }
    
    data.append(new_entry)
    
    with open(category_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print_success(f"Added '{args.saas}' → '{args.alternative}' to {category}")
    print_info("Submit a pull request to contribute this to the main repository!")


def cmd_verify(args: argparse.Namespace) -> None:
    """Verify an alternative entry exists and has proper metadata."""
    all_data = load_all_data()
    query = args.tool.lower()
    
    for category, tools in all_data.items():
        for tool in tools:
            saas_name = tool.get('saas_tool', {}).get('name', '').lower()
            alt_name = tool.get('alternative', {}).get('name', '').lower()
            
            if query in saas_name or query in alt_name or query in tool.get('description', '').lower():
                saas = tool.get('saas_tool', {})
                alt = tool.get('alternative', {})
                
                print(f"\n{Colors.BOLD}Verification Results:{Colors.END}")
                print(f"{Colors.CYAN}SaaS Tool:{Colors.END} {saas.get('name', 'Unknown')}")
                print(f"{Colors.CYAN}URL:{Colors.END} {saas.get('url', 'Not provided')}")
                print(f"\n{Colors.CYAN}Self-Hosted Alternative:{Colors.END} {alt.get('name', 'Unknown')}")
                print(f"{Colors.CYAN}URL:{Colors.END} {alt.get('url', 'Not provided')}")
                print(f"{Colors.CYAN}License:{Colors.END} {alt.get('license', 'Unknown')}")
                print(f"{Colors.CYAN}Docker:{Colors.END} {'Official image' if alt.get('docker', {}).get('official') else 'Custom'}")
                print(f"{Colors.CYAN}Category:{Colors.END} {category}")
                
                issues = []
                if not saas.get('url'):
                    issues.append("SaaS tool URL missing")
                if not alt.get('url'):
                    issues.append("Alternative URL missing")
                if not alt.get('docker', {}).get('official'):
                    issues.append("No official Docker image confirmed")
                
                if issues:
                    print(f"\n{Colors.YELLOW}Potential Issues:{Colors.END}")
                    for issue in issues:
                        print(f"  - {issue}")
                else:
                    print(f"\n{Colors.GREEN}✓ Entry looks good!{Colors.END}")
                
                return
    
    print_error(f"Tool '{args.tool}' not found in catalog")


def cmd_backup(args: argparse.Namespace) -> None:
    """Create a backup of all data."""
    import shutil
    from datetime import datetime
    
    data_path = get_data_path()
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_path = data_path.parent / "backups" / backup_name
    
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(data_path, backup_path)
    
    print_success(f"Backup created at {backup_path}")


def cmd_stats(args: argparse.Namespace) -> None:
    """Show statistics about the catalog."""
    all_data = load_all_data()
    
    total_tools = sum(len(tools) for tools in all_data.values())
    with_docker = 0
    with_license = 0
    categories = len(all_data)
    
    for tools in all_data.values():
        for tool in tools:
            alt = tool.get('alternative', {})
            if alt.get('docker', {}).get('official'):
                with_docker += 1
            if alt.get('license'):
                with_license += 1
    
    print(f"\n{Colors.BOLD}Catalog Statistics:{Colors.END}")
    print(f"  {Colors.CYAN}Total Entries:{Colors.END} {total_tools}")
    print(f"  {Colors.CYAN}Categories:{Colors.END} {categories}")
    print(f"  {Colors.GREEN}With Docker:{Colors.END} {with_docker} ({with_docker/total_tools*100:.1f}%)")
    print(f"  {Colors.GREEN}With License:{Colors.END} {with_license} ({with_license/total_tools*100:.1f}%)")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog='selfhosted',
        description='CLI tool for self-hosted alternatives catalog'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for tools')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--category', '-c', help='Filter by category')
    search_parser.add_argument('--format', '-f', choices=['table', 'json'], default='table')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List tools')
    list_parser.add_argument('--category', '-c', help='Filter by category')
    list_parser.add_argument('--format', '-f', choices=['table', 'csv'], default='table')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new tool')
    add_parser.add_argument('--saas', required=True, help='SaaS tool name')
    add_parser.add_argument('--saas-url', help='SaaS tool URL')
    add_parser.add_argument('--alternative', required=True, help='Self-hosted alternative name')
    add_parser.add_argument('--alt-url', help='Alternative URL')
    add_parser.add_argument('--category', '-c', default='general', help='Category')
    add_parser.add_argument('--license', '-l', default='MIT', help='License')
    add_parser.add_argument('--no-docker', action='store_true', help='No Docker image available')
    add_parser.add_argument('--docker-image', help='Docker image name')
    add_parser.add_argument('--docker-tag', help='Docker image tag')
    add_parser.add_argument('--cloud-only', action='store_true', help='Cloud-only version available')
    add_parser.add_argument('--description', help='Tool description')
    add_parser.add_argument('--contributor', help='Contributor name')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify a tool entry')
    verify_parser.add_argument('tool', help='Tool name to verify')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create data backup')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show catalog statistics')
    
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    commands = {
        'search': cmd_search,
        'list': cmd_list,
        'add': cmd_add,
        'verify': cmd_verify,
        'backup': cmd_backup,
        'stats': cmd_stats
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
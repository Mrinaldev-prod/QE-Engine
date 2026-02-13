#!/usr/bin/env python3
"""CLI to fetch a Jira issue and save it locally as JSON or print to stdout.

Reads Jira connection settings from environment variables or a .env file:
- JIRA_BASE_URL (e.g. https://yourorg.atlassian.net)
- JIRA_USER (email or username)
- JIRA_API_TOKEN (API token / password)

Usage:
  python jira_connector/cli_fetch_jira.py --issue KAN-1 --format json --out ./jira-KAN-1.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

import requests


def load_env_file(env_path: Optional[Path] = None) -> None:
    if load_dotenv is None:
        return
    if env_path and env_path.exists():
        load_dotenv(dotenv_path=str(env_path))
    else:
        # load from repo root .env if present
        root = Path(__file__).resolve().parents[1]
        env_file = root / '.env'
        if env_file.exists():
            load_dotenv(dotenv_path=str(env_file))


def get_jira_issue(issue_key: str) -> dict:
    base = os.environ.get('JIRA_BASE_URL')
    user = os.environ.get('JIRA_USER')
    token = os.environ.get('JIRA_API_TOKEN')
    if not base or not user or not token:
        raise RuntimeError('Missing Jira configuration. Set JIRA_BASE_URL, JIRA_USER, JIRA_API_TOKEN in environment or .env')

    api = base.rstrip('/') + f'/rest/api/2/issue/{issue_key}'
    params = { 'expand': 'renderedFields' }
    resp = requests.get(api, auth=(user, token), params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description='Fetch a Jira issue and save as JSON')
    parser.add_argument('--issue', '-i', required=True, help='Jira issue key (e.g. KAN-1)')
    parser.add_argument('--format', '-f', default='json', choices=['json', 'pretty'], help='Output format')
    parser.add_argument('--out', '-o', help='Output file path (if omitted prints to stdout)')
    parser.add_argument('--env-file', help='Path to .env file to load (optional)')

    args = parser.parse_args(argv)

    if args.env_file:
        load_env_file(Path(args.env_file))
    else:
        load_env_file()

    try:
        issue = get_jira_issue(args.issue)
    except Exception as e:
        print('Error fetching issue:', e, file=sys.stderr)
        return 2

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(json.dumps(issue, indent=2), encoding='utf-8')
        print(f'Wrote issue {args.issue} to {out_path}')
    else:
        if args.format == 'pretty':
            print(json.dumps(issue, indent=2))
        else:
            print(json.dumps(issue))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

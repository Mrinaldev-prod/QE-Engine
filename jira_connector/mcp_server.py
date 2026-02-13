#!/usr/bin/env python3
"""Tiny MCP-compatible HTTP server to fetch Jira issues on demand.

Provides a single endpoint:
  GET /jira/<issueKey>

Reads Jira credentials from environment or .env (same as the CLI).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

from flask import Flask, jsonify, make_response
import requests


def load_env_file(env_path: Optional[Path] = None) -> None:
    if load_dotenv is None:
        return
    if env_path and env_path.exists():
        load_dotenv(dotenv_path=str(env_path))
    else:
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
    resp = requests.get(api, auth=(user, token), params={'expand': 'renderedFields'}, timeout=30)
    resp.raise_for_status()
    return resp.json()


app = Flask(__name__)


@app.route('/jira/<issue_key>', methods=['GET'])
def jira_issue(issue_key: str):
    try:
        load_env_file()
        data = get_jira_issue(issue_key)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


def run(host: str = '127.0.0.1', port: int = 5002):
    app.run(host=host, port=port)


if __name__ == '__main__':
    run()

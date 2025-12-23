#!/usr/bin/env python3
"""Create a GitHub Pull Request using the repository's PR template.

Behavior:
- If the `gh` CLI is available, uses it to create the PR and passes the template as the body.
- Otherwise, if `GITHUB_TOKEN` is set, calls the GitHub REST API to open the PR using the template as the body.

Usage:
  python3 scripts/create_pr.py --title "My PR title" [--base main]

If `--title` is omitted, the script will derive a title from the current branch.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import urllib.error
from typing import Optional, Tuple


TEMPLATE_PATH = os.path.join('.github', 'PULL_REQUEST_TEMPLATE.md')


def read_template(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def current_branch() -> str:
    try:
        out = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], text=True).strip()
        return out
    except subprocess.CalledProcessError:
        return 'HEAD'


def remote_owner_repo() -> Optional[Tuple[str, str]]:
    try:
        url = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
    except subprocess.CalledProcessError:
        return None

    # handle git@github.com:owner/repo.git and https://github.com/owner/repo.git
    if url.startswith('git@'):
        # git@github.com:owner/repo.git
        parts = url.split(':', 1)[1]
    elif url.startswith('https://') or url.startswith('http://'):
        parts = url.split('/', 3)[-1]
    else:
        parts = url

    parts = parts.rstrip('.git')
    if '/' in parts:
        owner, repo = parts.split('/', 1)
        return owner, repo
    return None


def try_gh_cli(title: str, base: str, head: str, template_path: str) -> bool:
    gh = shutil.which('gh')
    if not gh:
        return False
    cmd = [gh, 'pr', 'create', '--title', title, '--body-file', template_path, '--base', base]
    # If head is not the current branch, pass it explicitly
    cmd += ['--head', head]
    print('Running:', ' '.join(cmd))
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        print('gh CLI failed:', e)
        return False


def create_pr_via_api(owner: str, repo: str, token: str, title: str, head: str, base: str, body: str) -> Optional[str]:
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    data = json.dumps({'title': title, 'head': head, 'base': base, 'body': body}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.load(resp)
            return resp_data.get('html_url')
    except urllib.error.HTTPError as e:
        try:
            err = e.read().decode()
            print('GitHub API error:', err)
        except Exception:
            print('GitHub API HTTPError:', e)
        return None
    except Exception as e:
        print('GitHub API request failed:', e)
        return None


def main():
    parser = argparse.ArgumentParser(description='Create a GitHub PR using the repository PR template.')
    parser.add_argument('--title', '-t', help='PR title (defaults to branch name)')
    parser.add_argument('--base', '-b', default=os.environ.get('BASE_BRANCH', 'main'), help='Base branch (default: main)')
    parser.add_argument('--head', help='Head branch (defaults to current branch)')
    args = parser.parse_args()

    head = args.head or current_branch()
    title = args.title or f'[{head}] Proposed changes'
    base = args.base

    template = read_template(TEMPLATE_PATH)
    if not template:
        print(f'Warning: PR template not found at {TEMPLATE_PATH}. Creating PR without template body.')

    # Try gh CLI first
    if try_gh_cli(title, base, head, TEMPLATE_PATH):
        print('PR created using gh CLI')
        return

    # Fall back to GitHub API if token is present
    token = os.environ.get('GITHUB_TOKEN')
    owner_repo = remote_owner_repo()
    if token and owner_repo:
        owner, repo = owner_repo
        body = template or ''
        print(f'Creating PR via GitHub API for {owner}/{repo} (head={head} base={base})')
        html = create_pr_via_api(owner, repo, token, title, head, base, body)
        if html:
            print('PR created:', html)
            return
        else:
            print('Failed to create PR via API')

    # If we reach here, we couldn't create the PR automatically
    print('\nAutomatic PR creation failed. Manual steps:')
    print('1) Ensure you have the GitHub CLI (https://cli.github.com/) installed and authenticated, then run:')
    print(f"   gh pr create --title '{title}' --body-file {TEMPLATE_PATH} --base {base} --head {head}")
    print('OR')
    print('2) Set the GITHUB_TOKEN environment variable (personal access token with repo scope) and re-run this script.')


if __name__ == '__main__':
    main()

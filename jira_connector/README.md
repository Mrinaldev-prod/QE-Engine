jira_connector
================

Small utilities to fetch Jira issues. There are two entry points:

- `cli_fetch_jira.py` - command-line tool to fetch a Jira issue and save it as JSON.
- `mcp_server.py` - tiny HTTP server (Flask) that exposes GET /jira/<issueKey> and returns the issue JSON.

Configuration
-------------
Provide the following environment variables (or put them in a `.env` file in the repo root):

- `JIRA_BASE_URL` - e.g. `https://yourorg.atlassian.net`
- `JIRA_USER` - your Jira email/username
- `JIRA_API_TOKEN` - your Jira API token or password

Examples
--------
CLI (write to file):

```
python jira_connector/cli_fetch_jira.py --issue KAN-1 --out jira-KAN-1.json
```

Run the small MCP server (for local use):

```
python jira_connector/mcp_server.py
# then request: http://127.0.0.1:5002/jira/KAN-1
```

Dependencies
------------
Install with:

```
pip install requests python-dotenv flask
```

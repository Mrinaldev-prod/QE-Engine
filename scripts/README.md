# PR creation helper

This folder contains a helper script to create pull requests pre-filled with the repository's PR template.

Usage

- Create a branch and push it to origin.
- Run the helper:

```bash
python3 scripts/create_pr.py --title "Add feature XYZ"
```

Behavior

- If the `gh` CLI (GitHub CLI) is installed and authenticated, the script will use it to create the PR and pass the template as the body.
- Otherwise, if the `GITHUB_TOKEN` environment variable is present, the script will call the GitHub REST API to open the PR (requires repo scope).
- If neither method is available, the script prints manual instructions.

How this helps the Agent

When you ask the assistant to create a PR, it will use this helper (if available) to consistently fill the PR template and create the PR. Ensure `gh` or `GITHUB_TOKEN` is configured on the machine where the assistant runs to allow automatic PR creation.

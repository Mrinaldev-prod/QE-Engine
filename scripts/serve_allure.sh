#!/usr/bin/env bash
set -euo pipefail

# Regenerate the Allure HTML report and serve it on localhost:8000
# Usage: ./scripts/serve_allure.sh [port]

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$ROOT_DIR/results/allure-results"
REPORT_DIR="$ROOT_DIR/results/allure-report"
PORT="${1:-8000}"

echo "Generating Allure report from: $RESULTS_DIR -> $REPORT_DIR"
if command -v allure >/dev/null 2>&1; then
  allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean
else
  echo "Allure CLI not found; ensure 'allure' is installed to regenerate the report."
fi

echo "Starting HTTP server to serve $REPORT_DIR on http://localhost:$PORT"
cd "$REPORT_DIR"

# Use nohup to keep server running in background and write logs
nohup python3 -m http.server "$PORT" > "$ROOT_DIR/results/allure-server.log" 2>&1 &
PID=$!
echo "Allure server started (pid=$PID). Logs: $ROOT_DIR/results/allure-server.log"
echo "Open: http://localhost:$PORT"

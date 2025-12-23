#!/usr/bin/env bash
set -euo pipefail

# Simple script to run different test scopes and collect Allure results and logs.
# Creates a timestamped run log at results/run_<timestamp>.log and attempts to
# generate an Allure HTML report after execution if the `allure` CLI is available.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$ROOT_DIR/results/allure-results"
REPORT_DIR="$ROOT_DIR/results/allure-report"
LOG_DIR="$ROOT_DIR/results"
mkdir -p "$RESULTS_DIR"
mkdir -p "$LOG_DIR"

# create timestamped run log
TS=$(date +%s)
RUN_LOG="$LOG_DIR/run_${TS}.log"
touch "$RUN_LOG"
echo "Run started: $(date -u)" | tee -a "$RUN_LOG"

run_py() {
  # helper to run python-based commands and tee output to the run log
  # usage: run_py <cmd...>
  echo "+ $*" | tee -a "$RUN_LOG"
  ("$@") 2>&1 | tee -a "$RUN_LOG"
  return ${PIPESTATUS[0]:-${PIPESTATUS[0]}}
}

case "${1:-all}" in
  unit)
    run_py python3 -m pytest --maxfail=1 -q --alluredir "$RESULTS_DIR"
    ;;
  smoke)
    # Ensure Playwright browsers are installed (best-effort)
    run_py python3 -m playwright install || true
    # Run behave via python -m to avoid PATH issues and send output to run log
    run_py python3 -m behave -f allure_behave.formatter:AllureFormatter -o "$RESULTS_DIR" tests/features/ui tests/features/api || true
    ;;
  e2e)
    run_py python3 -m playwright install || true
    run_py python3 -m behave -f allure_behave.formatter:AllureFormatter -o "$RESULTS_DIR" tests/features/mobile || true
    ;;
  all)
    run_py python3 -m pytest --maxfail=1 -q --alluredir "$RESULTS_DIR"
    run_py python3 -m playwright install || true
    run_py python3 -m behave -f allure_behave.formatter:AllureFormatter -o "$RESULTS_DIR" tests/features || true
    ;;
  *)
    echo "Unknown target. Usage: $0 [unit|smoke|e2e|all]" | tee -a "$RUN_LOG"
    exit 2
    ;;
esac

echo "Run finished: $(date -u)" | tee -a "$RUN_LOG"

# Try to generate Allure HTML report if the CLI is available
if command -v allure >/dev/null 2>&1; then
  echo "Generating Allure HTML report..." | tee -a "$RUN_LOG"
  rm -rf "$REPORT_DIR" || true
  allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean 2>&1 | tee -a "$RUN_LOG" || true
  echo "Allure report available at: $REPORT_DIR" | tee -a "$RUN_LOG"
else
  echo "Allure CLI not found; to generate HTML run: 'allure generate $RESULTS_DIR -o $REPORT_DIR --clean'" | tee -a "$RUN_LOG"
  echo "On macOS you can install with: brew install allure" | tee -a "$RUN_LOG"
fi

echo "Results (raw) are in $RESULTS_DIR" | tee -a "$RUN_LOG"
echo "Run log: $RUN_LOG"

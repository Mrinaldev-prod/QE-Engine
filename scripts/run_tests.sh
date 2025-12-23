#!/usr/bin/env bash
set -euo pipefail

# Simple script to run different test scopes and collect Allure results.
RESULTS_DIR=results/allure-results
mkdir -p "$RESULTS_DIR"

case "${1:-all}" in
  unit)
    pytest --maxfail=1 -q --alluredir "$RESULTS_DIR"
    ;;
  smoke)
    behave -k -f allure_behave.formatter:AllureFormatter -o "$RESULTS_DIR" tests/features/ui tests/features/api
    ;;
  e2e)
    behave -k -f allure_behave.formatter:AllureFormatter -o "$RESULTS_DIR" tests/features/mobile
    ;;
  all)
    pytest --maxfail=1 -q --alluredir "$RESULTS_DIR"
    behave -k -f allure_behave.formatter:AllureFormatter -o "$RESULTS_DIR" tests/features
    ;;
  *)
    echo "Unknown target. Usage: $0 [unit|smoke|e2e|all]"
    exit 2
    ;;
esac

echo "Results are in $RESULTS_DIR"

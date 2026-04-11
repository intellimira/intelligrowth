#!/bin/bash
# MIRA-Web-CLi OpenCode Bridge Launcher
# Usage: mira-bridge <url> [--auth] [--status <domain>]

VENV_PATH="/home/sir-v/Documents/MiRA-Web-CLi/src/.venv"
SCRIPT_PATH="/home/sir-v/MiRA/skills/lab-utility/scripts/mira_web_bridge.py"

# Activate venv and run
source "$VENV_PATH/bin/activate"
python3 "$SCRIPT_PATH" "$@"

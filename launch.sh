#!/usr/bin/env bash
# launch.sh - Launcher for Tarot Deck Studio Standalone App

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================================="
echo "  ✦ Launching Tarot Deck Studio..."
echo "=========================================================="

python3 server.py

#!/bin/bash

# Ensure we are in the script directory
cd "$(dirname "$0")"

# Check if tmux is installed
if ! command -v tmux &> /dev/null
then
    echo "tmux is not installed! Installing via Homebrew..."
    if command -v brew &> /dev/null
    then
        brew install tmux
    else
        echo "Error: Homebrew not found. Please install Homebrew or tmux manually."
        exit 1
    fi
fi

# Kill any existing session with this name to avoid duplicates
tmux kill-session -t watchlist-bot 2>/dev/null

# Start a new detached tmux session and run the python bot
tmux new-session -d -s watchlist-bot 'python3 main.py'

echo "==================================================="
echo "🟢 Bot successfully deployed 24/7 in the background!"
echo "It will continue running even if you close this terminal window."
echo ""
echo "To view the live output, type:"
echo "👉  tmux attach -t watchlist-bot"
echo ""
echo "To safely detach & leave it running in the background press: Ctrl+b, then d"
echo "==================================================="

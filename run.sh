#!/bin/bash
tmux kill-session -t dreamhack_leaderboard
tmux new-session -d -s dreamhack_leaderboard "python3 discordbot.py"

#!/bin/bash
# Start a DABT deep-dive session
# Usage: ./scripts/start-deep-dive.sh [topic]
# If topic is provided, the deep dive will target that subject
# Default: launches in deep-dive mode, loads current state

cd /home/vthen/work/dabt-tutor
hermes -w . -s dabt-deep-dive

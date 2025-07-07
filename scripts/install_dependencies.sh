#!/usr/bin/env bash
set -e

echo "This script will try to install FFmpeg and Tesseract OCR using your system's package manager."
read -rp "Proceed? [y/N] " answer
case "$answer" in
    [yY]*) ;;
    *) echo "Aborted."; exit 1;;
esac

# Detect package manager and run commands
if command -v brew >/dev/null 2>&1; then
    echo "Installing with Homebrew..."
    brew install ffmpeg tesseract
elif command -v apt-get >/dev/null 2>&1; then
    echo "Installing with apt-get..."
    sudo apt-get update
    sudo apt-get install -y ffmpeg tesseract-ocr
elif command -v winget >/dev/null 2>&1; then
    echo "Installing with winget..."
    winget install -e --id Gyan.FFmpeg
    winget install -e --id UB-Mannheim.Tesseract-OCR
else
    echo "Couldn't detect a supported package manager." >&2
    echo "Please install FFmpeg and Tesseract manually."
    exit 1
fi

echo "Installation finished."

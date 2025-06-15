#!/usr/bin/env bash

# Force Python 3.11 installation
echo "Installing Python 3.11..."
pyenv install 3.11.7
pyenv global 3.11.7

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!" 
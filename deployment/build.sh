#!/bin/bash

# Build script for Render deployment
echo "Starting build process..."

# Check Python version
python --version

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs

echo "Build completed successfully!" 
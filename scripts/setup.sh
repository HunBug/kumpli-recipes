#!/bin/bash

echo "Setting up Kumpli Recipes automation..."

# Make scripts executable
chmod +x scripts/optimize_images.py
chmod +x scripts/generate_ebook.py

# Install Python dependencies locally (optional)
if command -v pip3 &> /dev/null; then
    echo "Installing Python dependencies..."
    pip3 install --user Pillow
fi

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "Pandoc not found. Please install pandoc for e-book generation."
    echo "On Ubuntu/Debian: sudo apt-get install pandoc"
    echo "On macOS: brew install pandoc"
fi

echo "Setup complete!"
echo ""
echo "To test locally:"
echo "1. Run: python scripts/optimize_images.py"
echo "2. Run: python scripts/generate_ebook.py"
echo "3. Run: pandoc dist/kumpli-recipes.md -o dist/kumpli-recipes.epub"

#!/bin/bash
# Local build script for Kumpli Recipes
# Validates, generates, and creates EPUB locally

set -e  # Exit on error

RECIPES_DIR="${1:-recipes}"
OUTPUT_DIR="${2:-dist}"

echo "🔍 Validating recipes..."
python scripts/validate_recipes.py "$RECIPES_DIR"

echo ""
echo "📦 Generating HTML + Markdown + Images..."
python scripts/generate_from_json.py --input-dir "$RECIPES_DIR" --output-dir "$OUTPUT_DIR"

echo ""
echo "📚 Generating EPUB..."
cd "$OUTPUT_DIR"
pandoc kumpli-recipes.md -o kumpli-recipes.epub --metadata title="Kumpli Recipes" 2>/dev/null || echo "⚠️  Pandoc not found - skipping EPUB generation"
pandoc kumpli-recipes.md -o book.html --standalone --metadata title="Kumpli Recipes" --css style.css 2>/dev/null || echo "⚠️  Pandoc not found - skipping book.html generation"
cd ..

echo ""
echo "✅ Build complete!"
echo ""
echo "📂 Output in: $OUTPUT_DIR/"
echo "🌐 Preview: python -m http.server 8000 --directory $OUTPUT_DIR"

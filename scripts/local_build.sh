#!/usr/bin/env bash
set -euo pipefail

# Simple local build pipeline for Kumpli Recipes
# - Optimizes images (images/ -> optimized-images/)
# - Generates combined markdown and ToC (dist/)
# - Copies optimized images next to outputs (dist/optimized-images/)
# - Builds EPUB and standalone HTML (book.html)

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
IMG_DIR="${1:-images}"
RECIPES_DIR="${2:-recipes}"
OUT_DIR="${3:-dist}"
OPT_IMG_DIR="optimized-images"

cd "$ROOT_DIR"

info() { echo "[info] $*"; }
warn() { echo "[warn] $*"; }
err()  { echo "[error] $*" >&2; }

# 0) Check dependencies
command -v python3 >/dev/null 2>&1 || { err "python3 not found"; exit 1; }
if ! python3 -c 'import PIL' >/dev/null 2>&1; then
  warn "Pillow not found in current Python. Installing from requirements.txt..."
  python3 -m pip install -r requirements.txt
fi

if ! command -v pandoc >/dev/null 2>&1; then
  warn "pandoc not found. EPUB and HTML will not be built. Install with:"
  warn "  sudo apt-get update && sudo apt-get install -y pandoc"
fi

# 1) Optimize images
info "Optimizing images from '${IMG_DIR}' -> '${OPT_IMG_DIR}'..."
python3 scripts/optimize_images.py \
  --input-dir "${IMG_DIR}" \
  --output-dir "${OPT_IMG_DIR}"

# 2) Generate combined markdown + ToC
info "Generating combined markdown and ToC into '${OUT_DIR}'..."
python3 scripts/generate_ebook.py \
  --input-dir "${RECIPES_DIR}" \
  --output-dir "${OUT_DIR}" \
  --optimized-images "${OPT_IMG_DIR}"

# 3) Ensure CSS exists
mkdir -p "${OUT_DIR}"
if [ ! -f "${OUT_DIR}/style.css" ]; then
  info "Writing default CSS to '${OUT_DIR}/style.css'..."
  cat > "${OUT_DIR}/style.css" << 'EOF'
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
}
img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
h1, h2, h3 {
  color: #2c3e50;
}
code {
  background-color: #f8f9fa;
  padding: 2px 4px;
  border-radius: 3px;
}
pre {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
}
EOF
fi

# 4) Copy optimized images next to outputs for pandoc/HTML
info "Copying optimized images to '${OUT_DIR}/optimized-images/'..."
mkdir -p "${OUT_DIR}/optimized-images"
rsync -a --delete "${OPT_IMG_DIR}/" "${OUT_DIR}/optimized-images/" || true

# 5) Build EPUB and standalone HTML if pandoc exists
if command -v pandoc >/dev/null 2>&1; then
  info "Building EPUB..."
  pandoc "${OUT_DIR}/kumpli-recipes.md" \
    -o "${OUT_DIR}/kumpli-recipes.epub" \
    --metadata title="Kumpli Recipes"

  info "Building standalone HTML (book.html)..."
  pandoc "${OUT_DIR}/kumpli-recipes.md" \
    -o "${OUT_DIR}/book.html" \
    --standalone \
    --metadata title="Kumpli Recipes" \
    --css style.css
else
  warn "Skipping EPUB/HTML build (pandoc not installed)."
fi

info "Done. Preview locally with:"
info "  python3 -m http.server -d '${OUT_DIR}' 8000"
info "Then open http://localhost:8000/ in your browser."

# Kumpli Recipes Automation Setup

This setup automatically optimizes images, generates e-books, and publishes your recipes to GitHub Pages.

## Quick Start

1. Run the setup script:
```bash
./scripts/setup.sh
```

2. Set up GitHub deployment token:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Create a token with `repo` permissions
   - Add it as a repository secret named `DEPLOY_TOKEN`

3. Push to main branch - automation will run automatically!

## What it does

- **Image Optimization**: Converts PNG/JPEG to optimized JPEG (85% quality, max 1200px width), preserves EXIF orientation, progressive JPEG, skips up-to-date files
- **E-book Generation**: Combines markdown from `recipes/` into one file and builds EPUB + HTML
- **GitHub Pages**: Publishes HTML, EPUB, and optimized images to the external repo `HunBug/HunBug.github.io` under the `recipes/` folder on the `main` branch

## Local Testing

Fast path (recommended)

Use the helper script to build everything locally in one go:
```bash
./scripts/local_build.sh
# or customize source dirs
./scripts/local_build.sh images recipes dist
```
Then preview locally:
```bash
python3 -m http.server -d dist 8000
# open http://localhost:8000/
```

Manual steps

Optimize images (defaults to `images/` → `optimized-images/`):
```bash
python scripts/optimize_images.py --input-dir images --output-dir optimized-images
```

Generate e-book (reads from `recipes/`, writes to `dist/`):
```bash
python scripts/generate_ebook.py --input-dir recipes --output-dir dist --optimized-images optimized-images
```

Generate EPUB and standalone HTML (requires pandoc):
```bash
# Ensure images are visible to pandoc/HTML
rsync -a optimized-images/ dist/optimized-images/
# Build outputs
pandoc dist/kumpli-recipes.md -o dist/kumpli-recipes.epub --metadata title="Kumpli Recipes"
pandoc dist/kumpli-recipes.md -o dist/book.html --standalone --metadata title="Kumpli Recipes" --css style.css
```

Troubleshooting
- Missing images in EPUB: make sure `dist/optimized-images/` exists (copy via rsync above) or run `./scripts/local_build.sh`.
- Pandoc not installed: `sudo apt-get update && sudo apt-get install -y pandoc` (Ubuntu/Debian).
- No recipes found: ensure markdown files live under `recipes/`.

## File Structure

```
├── .github/workflows/build-and-deploy.yml  # GitHub Actions workflow
├── scripts/
│   ├── optimize_images.py                  # Image optimization script
│   ├── generate_ebook.py                   # E-book generation script
│   └── setup.sh                            # Setup script
├── dist/                                   # Generated files (HTML, EPUB)
├── optimized-images/                       # Optimized images (not committed)
├── images/                                 # Source images
└── recipes/                                # Source markdown files
```

## Output

After successful deployment, your content will be available at:
- Website: https://hunbug.github.io/recipes/
- E-book: https://hunbug.github.io/recipes/kumpli-recipes.epub

Only markdown files under `recipes/` are included in the book. Images should live under `images/`, and will be referenced from `optimized-images/` in the output.

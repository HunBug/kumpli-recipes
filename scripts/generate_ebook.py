#!/usr/bin/env python3
import os
import re
import argparse
from typing import List, Any, Tuple


def collect_markdown_files(directory: str) -> List[str]:
    """Collect all markdown files recursively"""
    md_files: List[str] = []
    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") and file.lower() != "readme.md":
                md_files.append(os.path.join(root, file))
    return sorted(md_files)


def slugify(text: str) -> str:
    """Create a URL-friendly slug from a string."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug


def process_markdown_content(
    content: str,
    base_path: str,
    optimized_images_path: str,
) -> str:
    """Process markdown content to use optimized images"""

    def replace_image(match: Any) -> str:
        alt_text = match.group(1)
        image_path = match.group(2).strip()
        # Leave already-optimized links untouched
        if image_path.startswith("optimized-images/") or image_path.startswith(
            "./optimized-images/"
        ):
            return match.group(0)
        # Normalize and strip extension
        without_ext, _ = os.path.splitext(image_path)
        # Remove leading ./
        while without_ext.startswith("./"):
            without_ext = without_ext[2:]
        # Strip leading images/ prefix so output path matches
        # the structure created by optimize_images.py
        if without_ext.startswith("images/"):
            without_ext = without_ext[len("images/"):]
        optimized_path = f"{optimized_images_path}/{without_ext}.jpg"
        return f"![{alt_text}]({optimized_path})"

    # Pattern to match markdown images: ![alt](path.ext)
    content = re.sub(
        r"!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg))\)",
        replace_image,
        content,
        flags=re.IGNORECASE,
    )

    return content


def generate_epub_structure(
    md_files: List[str],
    output_dir: str,
    optimized_images_path: str,
) -> Tuple[str, List[Tuple[str, str]]]:
    """Generate EPUB-friendly structure and collect ToC items.

    Returns a tuple of (combined_markdown_path, toc_items), where
    toc_items is a list of (title, slug).
    """
    os.makedirs(output_dir, exist_ok=True)

    # Create combined markdown file
    combined_content: List[str] = []
    combined_content.append("# Kumpli Recipes\n\n")

    toc_items: List[Tuple[str, str]] = []

    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Process content
        processed_content = process_markdown_content(
            content, md_file, optimized_images_path
        )

        # Add file as chapter with a stable anchor based on filename
        base = os.path.splitext(os.path.basename(md_file))[0]
        chapter_title = base.replace("_", " ").replace("-", " ").title()
        chapter_slug = slugify(base)
        toc_items.append((chapter_title, chapter_slug))
        combined_content.append(f"## {chapter_title} {{#{chapter_slug}}}\n\n")
        combined_content.append(processed_content)
        combined_content.append("\n\n---\n\n")

    # Write combined file
    output_file = os.path.join(output_dir, "kumpli-recipes.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(combined_content))

    return output_file, toc_items


def write_toc_html(toc_items: List[Tuple[str, str]], output_dir: str) -> str:
    """Write a simple ToC HTML linking to book.html and EPUB."""
    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, "index.html")

    items_html = "\n".join(
        f'      <li><a href="book.html#{slug}">{title}</a></li>'
        for title, slug in toc_items
    )

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kumpli Recipes</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header>
    <h1>Kumpli Recipes</h1>
    <p>
      <a href="kumpli-recipes.epub">Download EPUB</a>
      &middot; <a href="book.html">Read Online</a>
    </p>
  </header>
  <main>
    <h2>Table of Contents</h2>
    <ul>
{items_html}
    </ul>
  </main>
</body>
</html>
""".strip().replace("{items_html}", items_html)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return html_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate e-book from markdown files"
    )
    parser.add_argument(
        "--input-dir",
        default="recipes",
        help="Input directory with markdown files (default: recipes)",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Output directory",
    )
    parser.add_argument(
        "--optimized-images",
        default="optimized-images",
        help="Optimized images directory",
    )

    args = parser.parse_args()

    # Collect markdown files
    md_files = collect_markdown_files(args.input_dir)
    print(f"Found {len(md_files)} markdown files")

    # Generate EPUB structure and ToC items
    combined_md, toc_items = generate_epub_structure(
        md_files, args.output_dir, args.optimized_images
    )
    print(f"Generated combined markdown: {combined_md}")

    # Write ToC HTML (index.html)
    toc_html = write_toc_html(toc_items, args.output_dir)
    print(f"Generated ToC HTML: {toc_html}")


if __name__ == "__main__":
    main()

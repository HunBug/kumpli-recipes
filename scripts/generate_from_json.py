#!/usr/bin/env python3
"""
Generate e-book from recipe.json + story.md structure using Jinja2 templates.
Reads folders with recipe*.json and story.md, generates combined markdown + individual HTML pages.

Usage:
    python scripts/generate_from_json.py --input-dir recipes --output-dir dist
"""

import os
import json
import re
import argparse
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from PIL import Image, ImageOps

try:
    import markdown
except ImportError:
    print("❌ Error: markdown library not installed")
    print("Install with: pip install markdown")
    sys.exit(1)


# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Configuration constants for the recipe generator."""
    
    # Directory paths
    TEMPLATE_DIR = "templates"
    RAW_RECIPES_DIR = "raw_recipes"
    IMAGES_DIR = "images"
    
    # Template file names
    TEMPLATE_RECIPE_MD = "recipe.md.j2"
    TEMPLATE_CHAPTER_MD = "chapter.md.j2"
    TEMPLATE_BOOK_MD = "book.md.j2"
    TEMPLATE_INDEX_HTML = "index.html.j2"
    TEMPLATE_RECIPE_PAGE_HTML = "recipe-page.html.j2"
    TEMPLATE_RAW_RECIPE_PAGE_HTML = "raw-recipe-page.html.j2"
    TEMPLATE_STYLE_CSS = "style.css"
    
    # Output file names
    OUTPUT_COMBINED_MD = "kumpli-recipes.md"
    OUTPUT_INDEX_HTML = "index.html"
    
    # Image optimization defaults
    DEFAULT_IMAGE_QUALITY = 85
    DEFAULT_IMAGE_MAX_WIDTH = 1200
    
    # File patterns
    RECIPE_JSON_PREFIX = "recipe"
    STORY_FILE = "story.md"
    IMAGE_EXTENSIONS = ["*.png", "*.jpg", "*.jpeg"]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def slugify(text: str) -> str:
    """Create a URL-friendly slug from a string."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug


def optimize_image(
    input_path: str,
    output_path: str,
    quality: int = 85,
    max_width: int = 1200,
) -> bool:
    """
    Optimize a single image (resize, compress, convert to JPEG).
    Returns True if successful, False otherwise.
    """
    try:
        with Image.open(input_path) as img:
            # Honor EXIF orientation
            img = ImageOps.exif_transpose(img)

            # Convert RGBA/LA to RGB if necessary
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Resize if too wide
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize(
                    (max_width, new_height),
                    Image.Resampling.LANCZOS,
                )

            # Save optimized image
            out_dir = os.path.dirname(output_path)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
            icc = img.info.get("icc_profile")
            save_kwargs: Dict[str, Any] = {
                "quality": quality,
                "optimize": True,
                "progressive": True,
            }
            if icc:
                save_kwargs["icc_profile"] = icc
            img.save(output_path, **save_kwargs)

            return True
    except Exception as e:
        print(f"Warning: Could not optimize image {input_path}: {e}")
        return False


def process_recipe_images(
    recipe_folder: Path,
    output_dir: str,
    quality: int = 85,
    max_width: int = 1200,
) -> int:
    """
    Process all images in a recipe folder, optimizing them to {output_dir}/images/recipes/{slug}/.
    Returns the number of images processed.
    """
    processed = 0
    # Gather all image files
    image_files = []
    for ext in Config.IMAGE_EXTENSIONS:
        image_files.extend(recipe_folder.glob(ext))
    
    recipe_slug = recipe_folder.name
    images_output_dir = os.path.join(output_dir, Config.IMAGES_DIR, "recipes", recipe_slug)
    
    for image_file in image_files:
        # Change extension to .jpg for optimized version
        name_without_ext = image_file.stem
        output_path = os.path.join(images_output_dir, name_without_ext + ".jpg")
        
        # Skip if up-to-date
        try:
            if os.path.exists(output_path):
                src_mtime = os.path.getmtime(str(image_file))
                out_mtime = os.path.getmtime(output_path)
                if out_mtime >= src_mtime:
                    continue
        except OSError:
            pass
        
        if optimize_image(str(image_file), output_path, quality, max_width):
            processed += 1
            print(f"  Optimized: {image_file.name} -> {Config.IMAGES_DIR}/recipes/{recipe_slug}/{name_without_ext}.jpg")
    
    return processed


def discover_recipe_folders(directory: str) -> List[Path]:
    """Discover all folders containing recipe*.json files."""
    recipe_folders = set()
    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.startswith(Config.RECIPE_JSON_PREFIX) and file.endswith('.json'):
                recipe_folders.add(Path(root))
    return sorted(recipe_folders)


def load_recipe(recipe_file: Path) -> Dict[str, Any]:
    """Load and parse a recipe JSON file."""
    with open(recipe_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_story(story_file: Path) -> Dict[str, str]:
    """
    Load story.md content and parse into sections.
    Returns dict with section names as keys (e.g., 'Background', 'Kumpli Notes', 'Cooking Moments').
    """
    if not story_file.exists():
        return {}
    
    with open(story_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by H2 sections (## Header)
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections


def setup_jinja_env(template_dir: str = None) -> Environment:
    """Setup Jinja2 environment with templates."""
    if template_dir is None:
        template_dir = Config.TEMPLATE_DIR
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True
    )
    # Add markdown filter for converting markdown syntax to HTML
    env.filters['markdown'] = lambda text: markdown.markdown(text)
    return env


def process_image_paths(content: str, recipe_folder: Path, images_prefix: str, use_absolute_paths: bool = False) -> str:
    """Process image paths in story.md to point to optimized images."""
    
    def replace_image(match: Any) -> str:
        alt_text = match.group(1)
        image_path = match.group(2).strip()
        
        # If already an absolute path, leave it
        if image_path.startswith("/images/"):
            return match.group(0)
        
        # If already a relative images/ path and we need absolute, convert it
        if image_path.startswith("images/") or image_path.startswith("./images/"):
            if use_absolute_paths:
                clean_path = image_path.lstrip("./")
                return f"![{alt_text}](/{clean_path})"
            else:
                return match.group(0)
        
        # If it's a relative path in the recipe folder (like illustration.png, photo-1.png)
        if not image_path.startswith('../'):
            # Convert to images path using recipe folder structure
            recipe_slug = recipe_folder.name
            without_ext, _ = os.path.splitext(image_path)
            if use_absolute_paths:
                new_path = f"/{images_prefix}/recipes/{recipe_slug}/{without_ext}.jpg"
            else:
                new_path = f"{images_prefix}/recipes/{recipe_slug}/{without_ext}.jpg"
            return f"![{alt_text}]({new_path})"
        
        # Handle ../images/ paths
        abs_img = (recipe_folder / image_path).resolve()
        parts = abs_img.parts
        
        if "images" in parts:
            idx = parts.index("images")
            subparts = parts[idx + 1:]
            rel_under_images = "/".join(subparts)
        else:
            rel_under_images = image_path.lstrip('./')
        
        # Change extension to .jpg
        without_ext, _ = os.path.splitext(rel_under_images)
        if use_absolute_paths:
            new_path = f"/{images_prefix}/{without_ext}.jpg"
        else:
            new_path = f"{images_prefix}/{without_ext}.jpg"
        return f"![{alt_text}]({new_path})"
    
    # Pattern to match markdown images: ![alt](path.ext)
    content = re.sub(
        r"!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg))\)",
        replace_image,
        content,
        flags=re.IGNORECASE,
    )
    
    return content


def render_recipe_folder(
    recipe_folder: Path,
    optimized_images_path: str,
    jinja_env: Environment
) -> Tuple[str, str, str, Dict[str, Any]]:
    """
    Render a complete recipe folder (recipe*.json + story.md) using Jinja2.
    Returns (chapter_title, chapter_slug, markdown_content, recipe_data_for_html).
    """
    # Discover all recipe*.json files
    recipe_files = sorted(recipe_folder.glob(f'{Config.RECIPE_JSON_PREFIX}*.json'))
    
    if not recipe_files:
        return None
    
    # Load story.md and parse sections
    story_file = recipe_folder / Config.STORY_FILE
    story_sections = load_story(story_file)
    
    # Get modification times
    recipe_mtime = max(os.path.getmtime(f) for f in recipe_files)
    story_mtime = os.path.getmtime(story_file) if story_file.exists() else recipe_mtime
    last_modified = max(recipe_mtime, story_mtime)
    last_modified_date = datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d')
    
    # Process image paths in each story section
    for section_name, section_content in story_sections.items():
        story_sections[section_name] = process_image_paths(
            section_content, recipe_folder, optimized_images_path, use_absolute_paths=False
        )
    
    # Load all recipes
    recipes_data = []
    for recipe_file in recipe_files:
        recipe = load_recipe(recipe_file)
        recipes_data.append(recipe)
    
    # Render recipes for markdown
    recipe_template = jinja_env.get_template(Config.TEMPLATE_RECIPE_MD)
    rendered_recipes = []
    for recipe in recipes_data:
        rendered = recipe_template.render(recipe=recipe)
        rendered_recipes.append(rendered)
    
    # Use the first recipe's title as the chapter title
    first_recipe = recipes_data[0]
    chapter_title = first_recipe['title']
    chapter_slug = first_recipe['slug']
    
    # Render chapter using template
    chapter_template = jinja_env.get_template(Config.TEMPLATE_CHAPTER_MD)
    chapter_content = chapter_template.render(
        chapter_title=chapter_title,
        chapter_slug=chapter_slug,
        story_sections=story_sections,
        recipes=rendered_recipes,
        recipes_data=recipes_data  # For multi-recipe ToC
    )
    
    # Package data for HTML generation
    html_data = {
        'chapter_title': chapter_title,
        'chapter_slug': chapter_slug,
        'story_sections': story_sections,
        'recipes': recipes_data,
        'recipe_folder': recipe_folder,  # For reprocessing images with absolute paths
        'optimized_images_path': optimized_images_path,
        'last_modified': last_modified_date
    }
    
    return chapter_title, chapter_slug, chapter_content, html_data


def generate_combined_markdown(
    recipe_folders: List[Path],
    output_dir: str,
    optimized_images_path: str,
    jinja_env: Environment
) -> Tuple[str, List[Tuple[str, str]], List[Dict[str, Any]]]:
    """
    Generate combined markdown file and collect ToC items + recipe data using Jinja2.
    Returns (combined_markdown_path, toc_items, recipes_html_data).
    """
    os.makedirs(output_dir, exist_ok=True)
    
    chapters = []
    toc_items = []
    recipes_html_data = []
    
    for recipe_folder in recipe_folders:
        result = render_recipe_folder(recipe_folder, optimized_images_path, jinja_env)
        
        if result:
            chapter_title, chapter_slug, markdown_content, html_data = result
            toc_items.append((chapter_title, chapter_slug))
            chapters.append(markdown_content)
            recipes_html_data.append(html_data)
    
    # Render book using template
    book_template = jinja_env.get_template(Config.TEMPLATE_BOOK_MD)
    combined_content = book_template.render(chapters=chapters)
    
    # Write combined file
    output_file = os.path.join(output_dir, Config.OUTPUT_COMBINED_MD)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_content)
    
    return output_file, toc_items, recipes_html_data


def write_recipe_html_pages(recipes_html_data: List[Dict[str, Any]], output_dir: str, jinja_env: Environment) -> List[str]:
    """Generate individual HTML pages for each recipe."""
    os.makedirs(output_dir, exist_ok=True)
    
    recipe_template = jinja_env.get_template(Config.TEMPLATE_RECIPE_PAGE_HTML)
    generated_files = []
    
    for recipe_data in recipes_html_data:
        # Reprocess story sections with relative image paths for HTML
        story_sections_relative = {}
        recipe_folder = recipe_data.pop('recipe_folder')
        optimized_images_path = recipe_data.pop('optimized_images_path')
        
        for section_name, section_content in recipe_data['story_sections'].items():
            # Reprocess with relative paths (HTML is now at root level like markdown)
            story_sections_relative[section_name] = process_image_paths(
                section_content, recipe_folder, optimized_images_path, use_absolute_paths=False
            )
        
        # Convert markdown to HTML in story sections
        story_sections_html = {}
        for section_name, section_content in story_sections_relative.items():
            story_sections_html[section_name] = markdown.markdown(section_content)
        
        recipe_data['story_sections'] = story_sections_html
        
        # Add generation timestamp
        recipe_data['generated_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Generate HTML
        html_content = recipe_template.render(**recipe_data)
        
        # Write file
        output_file = os.path.join(output_dir, f"{recipe_data['chapter_slug']}.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        generated_files.append(output_file)
    
    return generated_files


def discover_raw_recipes(raw_recipes_dir: str = None) -> List[Dict[str, str]]:
    """Discover all markdown files in raw_recipes directory."""
    if raw_recipes_dir is None:
        raw_recipes_dir = Config.RAW_RECIPES_DIR
    raw_recipes = []
    if not os.path.exists(raw_recipes_dir):
        return raw_recipes
    
    for file in sorted(os.listdir(raw_recipes_dir)):
        if file.endswith('.md'):
            # Create title from filename
            title = file[:-3].replace('_', ' ').replace('-', ' ').title()
            slug = file[:-3]  # Remove .md extension
            raw_recipes.append({
                'title': title,
                'filename': file,
                'slug': slug,
                'path': os.path.join(raw_recipes_dir, file)
            })
    
    return raw_recipes


def generate_raw_recipe_html(raw_recipes: List[Dict[str, str]], output_dir: str, jinja_env: Environment) -> int:
    """Generate HTML pages from raw recipe markdown files."""
    if not raw_recipes:
        return 0
    
    generated = 0
    
    # Load the raw recipe template
    raw_template = jinja_env.get_template(Config.TEMPLATE_RAW_RECIPE_PAGE_HTML)
    
    for recipe in raw_recipes:
        # Read the markdown content
        with open(recipe['path'], 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(md_content)
        
        # Render the template
        page_html = raw_template.render(
            title=recipe['title'],
            content=html_content
        )
        
        # Write the HTML file
        output_file = os.path.join(output_dir, f"{recipe['slug']}.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(page_html)
        
        generated += 1
    
    return generated


def write_toc_html(toc_items: List[Tuple[str, str]], output_dir: str, jinja_env: Environment, raw_recipes: List[Dict[str, str]] = None) -> str:
    """Write a simple ToC HTML using Jinja2 template."""
    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, Config.OUTPUT_INDEX_HTML)

    # Render using template
    index_template = jinja_env.get_template(Config.TEMPLATE_INDEX_HTML)
    html_content = index_template.render(
        toc_items=toc_items,
        raw_recipes=raw_recipes or []
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_path


def copy_static_files(output_dir: str, template_dir: str = None) -> None:
    """Copy static files (CSS) from templates to output directory."""
    if template_dir is None:
        template_dir = Config.TEMPLATE_DIR
    
    css_source = os.path.join(template_dir, Config.TEMPLATE_STYLE_CSS)
    css_dest = os.path.join(output_dir, Config.TEMPLATE_STYLE_CSS)
    
    if os.path.exists(css_source):
        shutil.copy2(css_source, css_dest)
        print(f"Copied {Config.TEMPLATE_STYLE_CSS}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate e-book from recipe.json + story.md structure"
    )
    parser.add_argument(
        "--input-dir",
        default="recipes",
        help="Input directory with recipe folders (default: recipes)",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Output directory",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=Config.DEFAULT_IMAGE_QUALITY,
        help=f"JPEG quality for image optimization (1-100, default: {Config.DEFAULT_IMAGE_QUALITY})",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=Config.DEFAULT_IMAGE_MAX_WIDTH,
        help=f"Maximum width in pixels for image optimization (default: {Config.DEFAULT_IMAGE_MAX_WIDTH})",
    )

    args = parser.parse_args()

    # Setup Jinja2 environment
    jinja_env = setup_jinja_env()
    
    # Discover recipe folders
    recipe_folders = discover_recipe_folders(args.input_dir)
    print(f"Found {len(recipe_folders)} recipe folder(s)")

    # Process images for all recipe folders
    total_images = 0
    for recipe_folder in recipe_folders:
        processed = process_recipe_images(
            recipe_folder, args.output_dir, args.quality, args.max_width
        )
        total_images += processed
    if total_images > 0:
        print(f"Optimized {total_images} image(s)")

    # Generate combined markdown and ToC items
    combined_md, toc_items, recipes_html_data = generate_combined_markdown(
        recipe_folders, args.output_dir, Config.IMAGES_DIR, jinja_env
    )
    print(f"Generated combined markdown: {combined_md}")

    # Generate individual HTML pages
    html_pages = write_recipe_html_pages(recipes_html_data, args.output_dir, jinja_env)
    print(f"Generated {len(html_pages)} individual recipe HTML page(s)")

    # Discover raw recipes
    raw_recipes = discover_raw_recipes(Config.RAW_RECIPES_DIR)
    print(f"Found {len(raw_recipes)} raw recipe(s)")
    
    # Generate HTML pages for raw recipes
    if raw_recipes:
        generated_raw = generate_raw_recipe_html(raw_recipes, args.output_dir, jinja_env)
        print(f"Generated {generated_raw} raw recipe HTML page(s)")
    
    # Copy static files (CSS)
    copy_static_files(args.output_dir)
    
    # Write ToC HTML (index.html)
    toc_html = write_toc_html(toc_items, args.output_dir, jinja_env, raw_recipes)
    print(f"Generated ToC HTML: {toc_html}")


if __name__ == "__main__":
    main()

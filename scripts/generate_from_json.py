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
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from PIL import Image, ImageOps


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
    image_files = (
        list(recipe_folder.glob("*.png")) +
        list(recipe_folder.glob("*.jpg")) +
        list(recipe_folder.glob("*.jpeg"))
    )
    
    recipe_slug = recipe_folder.name
    images_output_dir = os.path.join(output_dir, "images", "recipes", recipe_slug)
    
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
            print(f"  Optimized: {image_file.name} -> images/recipes/{recipe_slug}/{name_without_ext}.jpg")
    
    return processed


def discover_recipe_folders(directory: str) -> List[Path]:
    """Discover all folders containing recipe*.json files."""
    recipe_folders = set()
    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('recipe') and file.endswith('.json'):
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


def setup_jinja_env(template_dir: str = "templates") -> Environment:
    """Setup Jinja2 environment with templates."""
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True
    )
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
    recipe_files = sorted(recipe_folder.glob('recipe*.json'))
    
    if not recipe_files:
        return None
    
    # Load story.md and parse sections
    story_file = recipe_folder / 'story.md'
    story_sections = load_story(story_file)
    
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
    recipe_template = jinja_env.get_template('recipe.md.j2')
    rendered_recipes = []
    for recipe in recipes_data:
        rendered = recipe_template.render(recipe=recipe)
        rendered_recipes.append(rendered)
    
    # Use the first recipe's title as the chapter title
    first_recipe = recipes_data[0]
    chapter_title = first_recipe['title']
    chapter_slug = first_recipe['slug']
    
    # Render chapter using template
    chapter_template = jinja_env.get_template('chapter.md.j2')
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
        'optimized_images_path': optimized_images_path
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
    book_template = jinja_env.get_template('book.md.j2')
    combined_content = book_template.render(chapters=chapters)
    
    # Write combined file
    output_file = os.path.join(output_dir, "kumpli-recipes.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_content)
    
    return output_file, toc_items, recipes_html_data


def write_recipe_html_pages(recipes_html_data: List[Dict[str, Any]], output_dir: str, jinja_env: Environment) -> List[str]:
    """Generate individual HTML pages for each recipe."""
    os.makedirs(output_dir, exist_ok=True)
    
    recipe_template = jinja_env.get_template('recipe-page.html.j2')
    generated_files = []
    
    # Try to import markdown, fallback to raw HTML if not available
    try:
        import markdown
        has_markdown = True
    except ImportError:
        has_markdown = False
    
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
        
        # Convert markdown to HTML in story sections if possible
        story_sections_html = {}
        for section_name, section_content in story_sections_relative.items():
            if has_markdown:
                story_sections_html[section_name] = markdown.markdown(section_content)
            else:
                # Simple fallback: wrap in <p> tags and convert line breaks
                story_sections_html[section_name] = '<p>' + section_content.replace('\n\n', '</p><p>').replace('\n', '<br>') + '</p>'
        
        recipe_data['story_sections'] = story_sections_html
        
        # Generate HTML
        html_content = recipe_template.render(**recipe_data)
        
        # Write file
        output_file = os.path.join(output_dir, f"{recipe_data['chapter_slug']}.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        generated_files.append(output_file)
    
    return generated_files


def write_toc_html(toc_items: List[Tuple[str, str]], output_dir: str, jinja_env: Environment) -> str:
    """Write a simple ToC HTML using Jinja2 template."""
    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, "index.html")

    # Render using template
    index_template = jinja_env.get_template('index.html.j2')
    html_content = index_template.render(toc_items=toc_items)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_path


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
        default=85,
        help="JPEG quality for image optimization (1-100, default: 85)",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1200,
        help="Maximum width in pixels for image optimization (default: 1200)",
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
        recipe_folders, args.output_dir, "images", jinja_env
    )
    print(f"Generated combined markdown: {combined_md}")

    # Generate individual HTML pages
    html_pages = write_recipe_html_pages(recipes_html_data, args.output_dir, jinja_env)
    print(f"Generated {len(html_pages)} individual recipe HTML page(s)")

    # Write ToC HTML (index.html)
    toc_html = write_toc_html(toc_items, args.output_dir, jinja_env)
    print(f"Generated ToC HTML: {toc_html}")


if __name__ == "__main__":
    main()

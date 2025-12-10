#!/usr/bin/env python3
"""
Generate template files for a new Kumpli recipe.

This script creates a new recipe folder with empty recipe.json and story.md templates.

Usage:
    python scripts/recipe_template_generator.py "Recipe Title"
    python scripts/recipe_template_generator.py "Recipe Title" --slug custom-slug
"""

import json
import sys
import re
from pathlib import Path
from typing import Optional


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters, keep alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Strip leading/trailing hyphens
    return text.strip('-')


def create_recipe_template(title: str, slug: Optional[str] = None) -> dict:
    """Create a recipe.json template with placeholder values."""
    if slug is None:
        slug = slugify(title)
    
    return {
        "title": title,
        "slug": slug,
        "emoji": "🍴",
        "metadata": {
            "cuisine": "TODO",
            "type": "TODO",
            "gluten_free": False,
            "difficulty": "Medium",
            "spicy": "None",
            "serves": "2-3 Kumplis",
            "good_for": ["comfort-food", "cooking-together"],
            "seasonality": "anytime",
            "ingredient_access": "standard-eu",
            "ingredient_count": 0,
            "storage": "TODO",
            "reheating": "TODO",
            "pairing": "TODO",
            "tags": ["soul-warming"]
        },
        "timing": {
            "prep_minutes": 0,
            "total_minutes": 0
        },
        "ingredients": [
            {
                "group": "Main Ingredients",
                "items": [
                    {
                        "amount": "TODO",
                        "item": "ingredient name",
                        "notes": "preparation notes"
                    }
                ]
            }
        ],
        "instructions": [
            {
                "title": "Step 1",
                "step": "Describe the first cooking step here."
            },
            {
                "step": "Continue with additional steps..."
            }
        ],
        "notes": "Optional: Add any special tips, variations, or Kumpli wisdom here."
    }


def create_story_template(title: str) -> str:
    """Create a story.md template with placeholder sections."""
    return f"""# Background

*Write the emotional, mythical, or personal introduction to the recipe here.*

Sometimes, in the Kumpli kitchen...

[Add Kumpli universe context, character references, and storytelling]

![Main illustration](illustration-1.png)
*Caption for the illustration*

## Kumpli Notes

*Add closing wisdom, serving suggestions, or character reactions here.*

Best enjoyed with [pairing suggestion]. [Character name] likes to [character behavior].

## Cooking Moments

![Photo of cooking process](photo-1.jpg)
*Caption describing the moment*

![Final plated dish](photo-2.jpg)
*The finished {title}*
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/recipe_template_generator.py \"Recipe Title\" [--slug custom-slug]")
        print("\nExample:")
        print("  python scripts/recipe_template_generator.py \"Boo's Legendary Stew\"")
        print("  python scripts/recipe_template_generator.py \"Maa's Forest Tea\" --slug forest-tea")
        sys.exit(1)
    
    title = sys.argv[1]
    
    # Check for custom slug
    custom_slug = None
    if "--slug" in sys.argv:
        slug_index = sys.argv.index("--slug")
        if slug_index + 1 < len(sys.argv):
            custom_slug = sys.argv[slug_index + 1]
    
    slug = custom_slug if custom_slug else slugify(title)
    
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    recipes_dir = project_root / "recipes"
    recipe_folder = recipes_dir / slug
    
    # Check if recipe already exists
    if recipe_folder.exists():
        print(f"❌ Recipe folder already exists: {recipe_folder}")
        print(f"   Choose a different title or slug")
        sys.exit(1)
    
    # Create recipe folder
    recipe_folder.mkdir(parents=True, exist_ok=True)
    
    # Create recipe.json
    recipe_data = create_recipe_template(title, slug)
    recipe_json_path = recipe_folder / "recipe.json"
    with open(recipe_json_path, 'w', encoding='utf-8') as f:
        json.dump(recipe_data, f, indent=2, ensure_ascii=False)
    
    # Create story.md
    story_content = create_story_template(title)
    story_md_path = recipe_folder / "story.md"
    with open(story_md_path, 'w', encoding='utf-8') as f:
        f.write(story_content)
    
    # Create .gitkeep for images (helps preserve folder structure)
    gitkeep_path = recipe_folder / ".gitkeep"
    gitkeep_path.touch()
    
    # Success message
    print(f"✅ Recipe template created successfully!")
    print(f"\n📁 Recipe folder: {recipe_folder}")
    print(f"   - recipe.json (structured data)")
    print(f"   - story.md (narrative & images)")
    print(f"\n📝 Next steps:")
    print(f"   1. Edit {recipe_json_path}")
    print(f"      - Fill in ingredients, instructions, and metadata")
    print(f"   2. Edit {story_md_path}")
    print(f"      - Write the background story and Kumpli notes")
    print(f"   3. Add images to {recipe_folder}/")
    print(f"      - illustration-1.png, photo-1.jpg, etc.")
    print(f"   4. Validate with: python scripts/validate_recipes.py {recipe_folder}")
    print(f"\n🎨 For ChatGPT assistance, see: gpt-instructions/")


if __name__ == "__main__":
    main()

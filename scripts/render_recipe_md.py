#!/usr/bin/env python3
"""
Simple Markdown renderer for testing recipe format.
Renders recipe.json to markdown to verify structure and formatting.

Usage:
    python scripts/render_recipe_md.py recipes/cozy-rum-hot-chocolate
"""

import json
import sys
from pathlib import Path


def render_ingredient(ingredient):
    """Render a single ingredient."""
    parts = []
    if ingredient.get('amount'):
        parts.append(ingredient['amount'])
    parts.append(ingredient['item'])
    result = ' '.join(parts)
    if ingredient.get('notes'):
        result += f" ({ingredient['notes']})"
    return result


def render_ingredients(ingredients):
    """Render ingredients section (supports grouped and flat)."""
    lines = []
    lines.append("## Ingredients\n")
    
    for item in ingredients:
        if 'group' in item:
            # Grouped ingredients
            lines.append(f"### {item['group']}\n")
            for ing in item['items']:
                lines.append(f"- {render_ingredient(ing)}")
            lines.append("")
        else:
            # Flat ingredient
            lines.append(f"- {render_ingredient(item)}")
    
    return '\n'.join(lines)


def render_instruction_step(step, indent_level=0):
    """Render a single instruction step with optional substeps."""
    lines = []
    indent = "  " * indent_level
    
    # Main step
    if step.get('title'):
        lines.append(f"{indent}**{step['title']}**: {step['step']}")
    else:
        lines.append(f"{indent}{step['step']}")
    
    # Substeps (variants)
    if step.get('substeps'):
        for substep in step['substeps']:
            sub_indent = "  " * (indent_level + 1)
            if substep.get('title'):
                lines.append(f"{sub_indent}* **{substep['title']}**: {substep['step']}")
            else:
                lines.append(f"{sub_indent}* {substep['step']}")
    
    return '\n'.join(lines)


def render_instructions(instructions):
    """Render instructions section (supports flat, grouped, and substeps)."""
    lines = []
    lines.append("## Instructions\n")
    
    step_counter = 1
    
    for item in instructions:
        if 'group' in item:
            # Grouped instructions
            lines.append(f"### {item['group']}\n")
            for step in item['steps']:
                lines.append(f"{step_counter}. {render_instruction_step(step)}")
                step_counter += 1
            lines.append("")
        else:
            # Flat instruction
            lines.append(f"{step_counter}. {render_instruction_step(item)}")
            step_counter += 1
    
    return '\n'.join(lines)


def render_recipe(recipe_path: Path):
    """Render a recipe.json file to markdown."""
    with open(recipe_path, 'r', encoding='utf-8') as f:
        recipe = json.load(f)
    
    lines = []
    
    # Title
    emoji = recipe.get('emoji', '')
    lines.append(f"# {recipe['title']} {emoji}\n")
    
    # Metadata
    meta = recipe['metadata']
    lines.append("## Metadata\n")
    lines.append(f"**Cuisine**: {meta['cuisine']}")
    lines.append(f"**Type**: {meta['type']}")
    lines.append(f"**Difficulty**: {meta['difficulty']}")
    lines.append(f"**Spicy**: {meta.get('spicy', 'N/A')}")
    lines.append(f"**Serves**: {meta['serves']}")
    lines.append("")
    
    # Timing
    timing = recipe['timing']
    lines.append("## Time\n")
    lines.append(f"**Prep**: {timing['prep_minutes']} minutes")
    lines.append(f"**Total**: {timing['total_minutes']} minutes")
    lines.append("")
    
    # Ingredients
    lines.append(render_ingredients(recipe['ingredients']))
    lines.append("")
    
    # Instructions
    lines.append(render_instructions(recipe['instructions']))
    
    return '\n'.join(lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/render_recipe_md.py recipes/recipe-folder")
        sys.exit(1)
    
    folder_path = Path(sys.argv[1])
    
    # Discover all recipe*.json files
    recipe_files = sorted(folder_path.glob('recipe*.json'))
    
    if not recipe_files:
        print(f"❌ No recipe files found in: {folder_path}")
        sys.exit(1)
    
    # Render all recipes with separator
    for i, recipe_file in enumerate(recipe_files):
        if i > 0:
            print("\n\n" + "="*80 + "\n\n")
        print(render_recipe(recipe_file))

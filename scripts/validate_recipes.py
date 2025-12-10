#!/usr/bin/env python3
"""
Validate Kumpli recipe JSON files against the schema.

This script provides non-blocking validation warnings for recipe.json files.
Validation failures do not prevent builds - creativity comes first!

Usage:
    python scripts/validate_recipes.py                    # Validate all recipes
    python scripts/validate_recipes.py recipes/my-recipe  # Validate specific recipe
    python scripts/validate_recipes.py --strict           # Exit with error on validation failures
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("❌ Error: jsonschema library not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)


class RecipeValidator:
    def __init__(self, schema_path: Path, sections_config_path: Path):
        """Initialize validator with schema file and story sections config."""
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)
        
        # Load story sections configuration
        with open(sections_config_path, 'r', encoding='utf-8') as f:
            sections_config = json.load(f)
            structure = sections_config.get('structure', {})
            
            self.allowed_h1_sections = set(structure.get('h1_sections', {}).get('allowed', []))
            h2_config = structure.get('h2_sections', {})
            self.required_h2_sections = set(h2_config.get('required', []))
            self.optional_h2_sections = set(h2_config.get('optional', []))
            self.allowed_h2_sections = self.required_h2_sections | self.optional_h2_sections
    
    def validate_recipe(self, recipe_path: Path) -> Tuple[bool, List[str]]:
        """
        Validate a single recipe.json file.
        
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        
        if not recipe_path.exists():
            return False, [f"Recipe file not found: {recipe_path}"]
        
        try:
            with open(recipe_path, 'r', encoding='utf-8') as f:
                recipe_data = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]
        
        try:
            validate(instance=recipe_data, schema=self.schema)
            return True, []
        except ValidationError as e:
            # Convert validation errors to readable warnings
            error_path = " -> ".join(str(p) for p in e.path) if e.path else "root"
            warning_msg = f"Validation warning at '{error_path}': {e.message}"
            warnings.append(warning_msg)
            return False, warnings
        except Exception as e:
            return False, [f"Unexpected validation error: {e}"]
    
    def validate_story_sections(self, story_path: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Validate story.md section structure.
        
        Returns:
            Tuple of (is_valid, list_of_errors, list_of_warnings)
        """
        errors = []
        warnings = []
        
        if not story_path.exists():
            return True, [], []  # story.md is optional, so no error if missing
        
        try:
            with open(story_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return False, [f"Could not read story.md: {e}"], []
        
        # Extract all H1 sections (# heading)
        h1_pattern = re.compile(r'^# (.+)$', re.MULTILINE)
        h1_sections = h1_pattern.findall(content)
        
        # Extract all H2 sections (## heading)
        h2_pattern = re.compile(r'^## (.+)$', re.MULTILINE)
        h2_sections = h2_pattern.findall(content)
        
        is_valid = True
        
        # Check for H1 sections (should not exist) - STRUCTURAL ERROR
        if h1_sections:
            is_valid = False
            errors.append(f"H1 sections (# heading) are not allowed in story.md. Found: {', '.join(h1_sections)}")
            errors.append("  → Change '# Background' to '## Background' (and any other H1 sections to H2)")
        
        # Check for required H2 sections - STRUCTURAL ERROR
        found_h2_set = set(h2_sections)
        missing_required = self.required_h2_sections - found_h2_set
        
        if missing_required:
            is_valid = False
            errors.append(f"Missing required sections in story.md: {', '.join(sorted(missing_required))}")
        
        # Check for unknown H2 sections - STRUCTURAL ERROR
        unknown_sections = found_h2_set - self.allowed_h2_sections
        
        if unknown_sections:
            is_valid = False
            errors.append(f"Unknown sections in story.md: {', '.join(sorted(unknown_sections))}")
            errors.append(f"  → Allowed sections are: {', '.join(sorted(self.allowed_h2_sections))}")
        
        return is_valid, errors, warnings
    
    def check_recipe_folder(self, folder_path: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Check a recipe folder for completeness and validity.
        Supports multiple recipe files: recipe.json, recipe.*.json
        
        Returns:
            Tuple of (is_valid, list_of_errors, list_of_warnings)
        """
        errors = []
        warnings = []
        story_md = folder_path / "story.md"
        
        # Find all recipe*.json files
        recipe_files = sorted(folder_path.glob("recipe*.json"))
        
        # Check for at least one recipe.json file - STRUCTURAL ERROR
        if not recipe_files:
            errors.append(f"No recipe*.json files found in {folder_path.name}")
            return False, errors, warnings
        
        # Validate primary recipe.json exists
        primary_recipe = folder_path / "recipe.json"
        if not primary_recipe.exists() and len(recipe_files) > 0:
            warnings.append(f"No primary recipe.json in {folder_path.name} - found only variants: {[f.name for f in recipe_files]}")
        
        # Missing story.md is just a warning
        if not story_md.exists():
            warnings.append(f"Missing story.md in {folder_path.name} (recommended but not required)")
        
        # Validate all recipe*.json files
        all_valid = True
        for recipe_file in recipe_files:
            is_valid, json_warnings = self.validate_recipe(recipe_file)
            if json_warnings:
                warnings.extend([f"[{recipe_file.name}] {w}" for w in json_warnings])
                all_valid = False
        
        # Validate story.md sections - errors for structure, warnings for content
        story_valid = True
        if story_md.exists():
            story_valid, story_errors, story_warnings = self.validate_story_sections(story_md)
            errors.extend(story_errors)
            warnings.extend(story_warnings)
        
        # Check for images - warning only
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        images = [f for f in folder_path.iterdir() 
                 if f.is_file() and f.suffix.lower() in image_extensions]
        
        if not images:
            warnings.append(f"No images found in {folder_path.name} (recipes are better with visuals!)")
        
        return all_valid and story_valid, errors, warnings


def find_recipe_folders(recipes_dir: Path) -> List[Path]:
    """Find all recipe folders (containing recipe.json)."""
    recipe_folders = []
    
    if not recipes_dir.exists():
        return recipe_folders
    
    for item in recipes_dir.iterdir():
        if item.is_dir() and (item / "recipe.json").exists():
            recipe_folders.append(item)
    
    return sorted(recipe_folders)


def main():
    strict_mode = "--strict" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    
    # Determine project root (script is in scripts/ folder)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    schema_path = project_root / "recipe.schema.json"
    sections_config_path = project_root / "reference" / "story-sections.json"
    recipes_dir = project_root / "recipes"
    
    # Check if schema exists
    if not schema_path.exists():
        print(f"❌ Schema not found: {schema_path}")
        sys.exit(1)
    
    # Check if story sections config exists
    if not sections_config_path.exists():
        print(f"❌ Story sections config not found: {sections_config_path}")
        sys.exit(1)
    
    # Initialize validator
    validator = RecipeValidator(schema_path, sections_config_path)
    
    # Determine what to validate
    if args:
        # Validate specific recipe(s)
        target_path = Path(args[0])
        if not target_path.is_absolute():
            target_path = project_root / target_path
        
        if target_path.is_dir():
            # If target is the recipes directory itself, find all recipe folders within it
            if target_path.resolve() == recipes_dir.resolve():
                recipe_folders = find_recipe_folders(recipes_dir)
            # Otherwise treat it as a single recipe folder
            else:
                recipe_folders = [target_path]
        else:
            print(f"❌ Not a directory: {target_path}")
            sys.exit(1)
    else:
        # Validate all recipes
        recipe_folders = find_recipe_folders(recipes_dir)
        
        if not recipe_folders:
            print(f"📭 No recipe folders found in {recipes_dir}")
    # Validate each recipe
    print(f"🔍 Validating {len(recipe_folders)} recipe(s)...\n")
    
    total_valid = 0
    total_errors = 0
    total_warnings = 0
    recipes_with_errors = []
    
    for folder in recipe_folders:
        recipe_name = folder.name
        is_valid, errors, warnings = validator.check_recipe_folder(folder)
        
        has_errors = len(errors) > 0
        has_warnings = len(warnings) > 0
        
        if not has_errors and not has_warnings:
            print(f"✅ {recipe_name}")
            total_valid += 1
        else:
            if has_errors:
                print(f"❌ {recipe_name}")
                recipes_with_errors.append(recipe_name)
                for error in errors:
                    print(f"   ERROR: {error}")
                total_errors += len(errors)
            elif has_warnings:
                print(f"⚠️  {recipe_name}")
            
            if has_warnings:
                for warning in warnings:
                    print(f"   WARNING: {warning}")
                total_warnings += len(warnings)
        print()
    
    # Summary
    print("─" * 60)
    print(f"📊 Validation Summary:")
    print(f"   Valid recipes: {total_valid}/{len(recipe_folders)}")
    print(f"   Total errors: {total_errors}")
    print(f"   Total warnings: {total_warnings}")
    
    if total_errors > 0:
        print(f"\n❌ ERRORS FOUND - These must be fixed!")
        print(f"   Recipes with errors: {', '.join(recipes_with_errors)}")
        print(f"   Errors are structural issues that will break HTML generation.")
    
    if total_warnings > 0:
        print(f"\n💡 Warnings: {total_warnings} found")
        print(f"   Warnings are guidelines, not rules. Creativity comes first!")
    
    # Exit with error if there are structural errors OR if strict mode with warnings
    if total_errors > 0:
        print(f"\n❌ Build failed due to {total_errors} error(s)")
        sys.exit(1)
    
    if strict_mode and total_warnings > 0:
        print(f"\n❌ Strict mode: Exiting with error due to {total_warnings} warning(s)")
        sys.exit(1)
    
    print(f"\n✅ All validations passed!")
    sys.exit(0)


if __name__ == "__main__":
    main()

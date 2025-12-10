# ChatGPT Instructions Update Plan

## Current State
- Old format: Single Markdown files with embedded frontmatter-style metadata
- Old image paths: `../images/illustrations/<slug>.png` and `../images/photos/<slug>-p1.png`
- Old structure: All content in one `.md` file

## New State (After Refactoring)
- New format: Separate `recipe.json` + `story.md` in folder structure
- New folder structure: `recipes/<slug>/recipe.json`, `recipes/<slug>/story.md`
- New image paths: Relative paths in story.md (e.g., `illustration.jpg`, `photo-1.jpg`)
- Images stored in: `images/recipes/<slug>/illustration.jpg`, `images/recipes/<slug>/photo-1.jpg`, etc.
- JSON schema with strict validation

## What Needs to be Updated

### 1. Recipe Instructions File
**Major Changes:**
- Replace Markdown template with JSON + story.md structure
- Update image path format (use simple filenames, not full paths)
- Add JSON schema reference
- Update metadata fields to match new schema (e.g., `spice_level` instead of text)
- Separate story sections from recipe data
- Add story.md template with sections: Background, Kumpli Notes, Cooking Moments

**Keep:**
- Creative diversity rules (A/B versions)
- Tone and style guidelines
- Character/setting palette
- Anti-repetition rules
- User-controlled style toggles

### 2. Illustration Instructions File
**Changes Needed:**
- Update filenames: `illustration.jpg` (not `<slug>.png`)
- Update photo filenames: `photo-1.jpg`, `photo-2.jpg`, etc. (not `<slug>-p1.png`)
- Explain that images go in `images/recipes/<slug>/` during generation
- Update image references in story.md (just filename, not path)
- Keep all scene/style/caption generation rules

### 3. New Files to Create
- **recipe-json-template.md**: Complete JSON structure with examples
- **story-md-template.md**: Story.md structure with all sections
- **folder-structure-guide.md**: How to organize files and where images go
- **migration-from-old-format.md**: (optional) For reference

## Next Steps
1. ✅ Move files to chatgpt-instructions folder
2. ✅ Create project-prompt.md
3. Update recipe-instructions-v2.0.md
4. Update illustration-instructions-v2.0.md
5. Create recipe-json-template.md
6. Create story-md-template.md
7. Create folder-structure-guide.md
8. Test with ChatGPT

## Key Schema Fields to Document

### recipe.json structure:
```
{
  "title": string,
  "slug": string,
  "emoji": string (optional),
  "metadata": {
    "cuisine": string,
    "type": string,
    "gluten_free": boolean (optional),
    "difficulty": string,
    "spice_level": string (optional),
    "serves": string,
    "good_for": array (optional),
    "seasonality": string (optional),
    "ingredient_access": string (optional),
    "storage": string (optional),
    "reheating": string (optional),
    "pairing": string (optional),
    "tags": array
  },
  "timing": {
    "prep_time": string,
    "total_time": string
  },
  "ingredients": [
    {
      "group": string (optional),
      "items": [
        {
          "amount": string,
          "item": string,
          "notes": string (optional)
        }
      ]
    }
  ],
  "instructions": [
    {
      "group": string (optional),
      "step": string,
      "title": string (optional),
      "substeps": array (optional)
    }
  ]
}
```

### story.md structure:
```markdown
# Background
[Story content with images]

# Kumpli Notes
[Cozy notes]

# Cooking Moments
## [Section Title]
![Alt text](photo-1.jpg)
*Caption*

## [Section Title]
![Alt text](photo-2.jpg)
*Caption*
```

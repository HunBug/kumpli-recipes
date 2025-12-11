# 📚 ChatGPT Instructions — README

This folder contains all the instructions and reference files needed to set up a ChatGPT Project for generating Kumpli Cookbook recipes.

## 📁 Files in This Folder

### Core Files (Upload to ChatGPT)
1. **00_QUICK_START.md** — Quick setup guide (read this first!)
2. **recipe-instructions-v2.0.md** — Complete recipe generation instructions
3. **illustration-instructions-v2.0.md** — Illustration and image handling instructions
4. **project-prompt.md** — Custom project instructions to paste into ChatGPT

### Reference Files
- **update-plan.md** — Technical documentation of the refactoring process

## 🚀 How to Use

### Step 1: Upload Files to ChatGPT Project

Create a new ChatGPT Project and upload these files:

**From `chatgpt-instructions/` folder:**
- `recipe-instructions-v2.0.md`
- `illustration-instructions-v2.0.md`

**From `conventions/` folder:**
- `recipe.schema.json`
- `story-sections.json`
- `tags.json`
- `spice-levels.md`
- `multi-recipe-variants.md`

**Example recipes (pick 2-3):**
- `recipes/cozy-rum-hot-chocolate/recipe.json`
- `recipes/cozy-rum-hot-chocolate/story.md`
- `recipes/tor-boo-s-kulmsupp/recipe.json`
- `recipes/tor-boo-s-kulmsupp/story.md`

### Step 2: Set Custom Instructions

Copy the content from `project-prompt.md` into the ChatGPT **Custom Instructions** field.

### Step 3: Initialize ChatGPT

Send the initialization prompt from `00_QUICK_START.md` to ChatGPT.

### Step 4: Start Creating Recipes!

ChatGPT will now generate:
- `recipe.json` files (validated against schema)
- `story.md` files (with proper sections)
- Illustration prompts with correct filenames

## 📖 What ChatGPT Will Generate

### recipe.json Structure
```json
{
  "title": "Recipe Name",
  "slug": "recipe-slug",
  "emoji": "🥘",
  "metadata": { ... },
  "timing": { ... },
  "ingredients": [ ... ],
  "instructions": [ ... ]
}
```

### story.md Structure
```markdown
## Background
[Story with illustration]

## Kumpli Notes
[Cozy final thoughts]

## Cooking Moments
[Optional photo captions]
```

### Images
- `illustration.jpg` — Main illustration
- `photo-1.jpg`, `photo-2.jpg` — Optional photos

## ✅ Validation

After generating recipes, validate them:

```bash
# Validate one recipe
python scripts/validate_recipes.py recipes/<slug>

# Build everything
./scripts/build_local.sh
```

## 🎨 Creative Features

ChatGPT will:
- ✨ Rotate styles and tones (cozy, mythic, surreal, etc.)
- 🌍 Use diverse Kumpli universe characters and settings
- 🎭 Offer creative A/B versions for backgrounds
- 📸 Generate illustration prompts with style/scene variants
- 🏷️ Suggest tags from vocabulary (creative freedom allowed)
- 🔄 Follow anti-repetition rules to keep content fresh

## 📋 Key Principles

1. **Two-file structure:** `recipe.json` + `story.md`
2. **Schema validation:** Must pass `recipe.schema.json`
3. **Simple image paths:** Use filenames only, not full paths
4. **Required story sections:** Background, Kumpli Notes (+ optional Cooking Moments)
5. **Creative diversity:** Rotate styles, characters, settings
6. **Production-ready:** Clean, structured, immediately usable

## 🔗 Related Documentation

- `/conventions/recipe.schema.json` — JSON schema for validation
- `/conventions/tags.json` — Tag vocabulary suggestions
- `/conventions/story-sections.json` — Story structure rules
- `/conventions/spice-levels.md` — Kumpli spice scale
- `/conventions/multi-recipe-variants.md` — Multi-recipe variants guide
- `/AUTOMATION_README.md` — Build system documentation

---

**Happy recipe creation! Cook with heart, write with warmth, and let the magic flow.** 🥔✨

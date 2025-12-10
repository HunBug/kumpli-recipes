# Recipe Compatibility Analysis
## JSON Schema vs. Existing Markdown Recipes

**Date:** 2025-12-08  
**Purpose:** Analyze all non-migrated recipes to identify features that may not be supported by the current JSON schema

---

## Executive Summary

✅ **Good News:** All recipe content CAN be preserved in the new JSON format  
✅ **Schema Enhancements Implemented:**
- **Grouped instructions** for recipe phases (prep → cook → assemble)
- **Substeps** for variants/alternatives within a single step
- **Multi-recipe folders** with `recipe.{variant}.json` naming convention
📝 **Minor Considerations:** Some recipes use creative H2 sections beyond the standard three (acceptable in story.md)

---

## Recipes Analyzed (9 total)

1. `choo-night-bibimbap-bowl.md`
2. `boos_smoky_burrito_of_bravery.md`
3. `peri-peri-livers-de-la-kukli.md`
4. `emergency_feast_of_eternal_laziness.md`
5. `savoy_snuggle_stack.md`
6. `batata_and_coconut_soup.md`
7. `tor-boo-s_kulmsupp.md`
8. `the_ultimate_okonomiyaki.md`
9. `seoul_smasher.md`

---

## Key Findings

### ✅ Fully Supported Features

All recipes contain these elements that are **already supported** by the current schema:

- **Grouped Ingredients** (e.g., "Bibimbap Bowl" → "Vegetables", "Protein", "Toppings")
- **Flat Ingredients** (simple lists)
- **Recipe Metadata** (cuisine, difficulty, spicy level, etc.)
- **Timing Information** (prep time, total time)
- **Tags and Good-For Lists**
- **Multiple Images** (illustrations + photos)
- **Emoji Representation**
- **Serves Information**

### ⚠️ Feature Gap: Grouped Instructions

**Current Schema:** Instructions are a flat array of steps  
**Real Usage:** Several recipes use **grouped/sectioned instructions**

#### Examples:

**Choo-Night Bibimbap Bowl:**
```markdown
## Instructions
1. **Make the Sauce**: ...
2. **Prep the Vegetables**: [subdivided into different veggies]
3. **Cook the Eggs**: ...
4. **Assemble the Bowl**: ...
```

**Boo's Smoky Burrito:**
```markdown
## Instructions
1. **Marinate the Steak:** ...
2. **Prepare Rice:** ...
3. **Char the Corn:** ...
4. **Cook the Beans:** ...
5. **Sear the Steak:** ...
```

**Seoul Smasher:**
Has a **variant recipe section** embedded in the same document:
```markdown
## Instructions
[Main Korean burger instructions]

---
## Classic OG Burger (No Korean Ingredients) — with Fried Corn
[Alternative variant instructions]
```

**Observation:** These grouped instructions help organize complex recipes into logical phases (prep → cook → assemble).

---

### 🎭 Story Section Creativity

Most recipes follow the standard H2 structure:
- `## Background`
- `## Kumpli Notes`
- `## 📸 Cooking Moments` (or variations like `## 🍚 Maa's Cozy Bibimbap and Miso`)

**Exceptions:**
- **Seoul Smasher** has multiple custom H2 sections within Cooking Moments:
  - `## 🍔 Two bites`
  - `## 🍔 Just for Him`
  - `## 🍔 Let It Wait`

**Current Schema:** Only validates that H2 sections match allowed list  
**Impact:** These creative subsections would be flagged as "unknown sections" by validator

**Recommendation:** Story.md is intentionally flexible for creativity. Validator should check top-level structure only, allowing freedom within narrative sections.

---

## Implemented Schema Enhancements

### 1. Grouped Instructions (for recipe phases)

**Status:** ✅ Implemented

Allows organizing complex recipes into logical phases:

```json
"instructions": [
  {
    "group": "Prepare the Sauce",
    "steps": [
      { "step": "Mix ingredients..." }
    ]
  },
  {
    "group": "Assembly",
    "steps": [
      { "step": "Combine everything..." }
    ]
  }
]
```

**Use for:** Distinct recipe phases like prep, cook, assembly

---

### 2. Substeps (for variants within a step)

**Status:** ✅ Implemented

Allows variants/alternatives within a single instruction step:

```json
{
  "title": "Finish the hot chocolate",
  "step": "Remove from heat and stir in vanilla.",
  "substeps": [
    {
      "title": "For Elf version",
      "step": "Add 1–2 tbsp rum per serving."
    },
    {
      "title": "For Small Kumpli version",
      "step": "Add a tiny pinch of chili."
    }
  ]
}
```

**Benefits:**
- Clear semantic distinction: `group` = phases, `substeps` = variations
- Same `{title, step}` structure everywhere - consistent parsing
- No nested groups (avoids complexity)
- Optional field - recipes without variants don't need it

**Use for:** Optional additions, serving variations, substitutions

---

### 3. Multi-Recipe Folders

**Status:** ✅ Implemented

**Naming Convention:**
- Primary: `recipe.json`
- Variants: `recipe.{variant-name}.json`

**Example:**
```
recipes/seoul-smasher/
├── recipe.json           # Korean fusion version
├── recipe.classic.json   # Classic OG burger
└── story.md              # Shared narrative
```

**Renderer discovers all `recipe*.json` files and renders in alphabetical order.**

**Use for:** Substantial variants with different ingredients/methods (>30% difference)

---

## Decision Framework

### When to use what:

**Flat instructions:**
- Simple linear recipes (≤10 steps)
- No distinct phases

**Grouped instructions:**
- Complex recipes with phases (prep → cook → assemble)
- Multiple components prepared separately
- Clear workflow stages

**Substeps:**
- Optional variants within a step
- Serving suggestions
- Simple substitutions
- Alternative flavorings

**Separate recipe files:**
- Ingredients differ significantly (>30%)
- Cooking method substantially different
- Each version deserves own title/identity

---

## Proposed Schema Enhancements (ARCHIVED - Now Implemented)

### Original Proposal for Grouped Instructions
```json
"instructions": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["step"],
    "properties": {
      "step": { "type": "string" },
      "title": { "type": "string" }
    }
  }
}
```

**Proposed Enhancement:**
```json
"instructions": {
  "oneOf": [
    {
      "type": "array",
      "description": "Flat list of instruction steps",
      "items": {
        "type": "object",
        "required": ["step"],
        "properties": {
          "step": { "type": "string" },
          "title": { "type": "string" }
        }
      }
    },
    {
      "type": "array",
      "description": "Grouped instruction steps (e.g., prep, cook, assemble)",
      "items": {
        "type": "object",
        "required": ["group", "steps"],
        "properties": {
          "group": { 
            "type": "string",
            "description": "Group name (e.g., 'Prepare Vegetables', 'Assembly')"
          },
          "steps": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["step"],
              "properties": {
                "step": { "type": "string" },
                "title": { "type": "string" }
              }
            }
          }
        }
      }
    }
  ]
}
```

**Benefits:**
- Maintains backward compatibility with flat instruction lists
- Supports logical grouping for complex recipes
- Matches the structure already used for grouped ingredients
- Makes templates more flexible for different presentation styles

---

### 2. Relaxed Story Section Validation

**Current Behavior:** Validator checks for exact H2 section names

**Recommendation:**
- Keep required sections: `Background`, `Kumpli Notes`
- Allow optional section: `Cooking Moments` (or variants with emoji)
- **Don't validate subsections within narrative areas** — creativity is key

**Rationale:** The story.md is where personality lives. As long as the structural foundation exists (Background, Kumpli Notes), the rest should be free-form.

---

## Migration Considerations

### Recipe Variants (Seoul Smasher case)

**Current Approach:** Recipe variants embedded in same markdown file

**JSON Options:**
1. **Single recipe with variant instructions** (grouped format handles this)
2. **Separate recipe files** (e.g., `seoul-smasher-korean/` and `seoul-smasher-classic/`)

**Recommendation:** Use grouped instructions to show "Alternative Assembly" or create separate recipe files if variants are substantially different.

---

## Can We Regenerate Original from JSON?

**Answer: YES** ✅

With the proposed instruction grouping enhancement, we can regenerate:
- All metadata fields
- All ingredient lists (flat or grouped)
- All instruction steps (flat or grouped)
- All timing and serving information
- All tags and classifications

**What lives in story.md (not JSON):**
- Narrative backgrounds
- Kumpli personality and lore
- Cooking moment descriptions
- Character anecdotes

**Conclusion:** The separation is clean and lossless. JSON holds recipe data; story.md holds soul.

---

## Recommendations Summary

### High Priority
✅ **Add grouped instructions support** to match grouped ingredients pattern

### Medium Priority
⚠️ **Update validator** to allow creative H2 subsections within story.md

### Low Priority (Future)
- Consider how to handle recipe variants (documentation or tooling)
- Template design should support both flat and grouped instruction rendering

---

## Migration Readiness

**Status:** READY ✅

All recipes can be migrated once instruction grouping is added to schema. No content will be lost. The structure is flexible enough to preserve all information and creativity.

**Next Steps:**
1. Update `recipe.schema.json` with grouped instructions support
2. Update migration guide with grouped instruction examples
3. Proceed with Phase 2 migrations

# Kumpli Recipe Format Reference

This document describes the JSON format for Kumpli Cookbook recipes after the repository refactoring.

## Overview

Each recipe consists of files stored in a dedicated folder:

```
recipes/
└── recipe-slug/
    ├── recipe.json              # Primary recipe (structured data)
    ├── recipe.variant-name.json # Optional: recipe variant (e.g., recipe.classic.json)
    ├── story.md                 # Background narrative, Kumpli notes, images
    ├── illustration.png         # Images referenced in story.md
    ├── photo-1.jpg
    └── ...
```

**Multi-Recipe Folders**: Folders can contain multiple recipe variants:
- Primary recipe: `recipe.json`
- Variants: `recipe.{variant-name}.json` (e.g., `recipe.classic.json`, `recipe.spicy.json`)
- Renderer will discover all `recipe*.json` files and render them in filename order
- All variants share the same `story.md` file

---

## File Structure

### `recipe.json`

Contains all structured recipe data: metadata, timing, ingredients, and cooking instructions.

**Validation**: Validated against `recipe.schema.json` (warnings only, non-blocking)

**Format**: JSON with pretty printing (2-space indentation)

---

## JSON Fields Reference

### Required Top-Level Fields

#### `title` (string, required)
Full display name of the recipe.

**Examples:**
```json
"title": "Boo's Smoky Burrito of Bravery"
"title": "The Ultimate Okonomiyaki"
```

#### `slug` (string, required)
URL-safe identifier matching the folder name. Lowercase, hyphens only, no spaces.

**Examples:**
```json
"slug": "boos-smoky-burrito-of-bravery"
"slug": "the-ultimate-okonomiyaki"
```

#### `emoji` (string, optional)
Emoji representation of the dish for visual flair.

**Examples:**
```json
"emoji": "🌯🔥"
"emoji": "🥞"
```

---

### `metadata` (object, required)

Recipe classification and characteristics.

#### Required Metadata Fields

- **`cuisine`** (string): Origin or style (e.g., `"Mexican-inspired"`, `"Japanese"`, `"Fusion"`)
- **`type`** (string): Dish category (e.g., `"Burrito"`, `"Main course"`, `"Dessert"`)
- **`difficulty`** (string): Cooking difficulty - creative freedom, common values: `"Easy"`, `"Medium"`, `"Hard"`
- **`serves`** (string): Number of servings, Kumpli style (e.g., `"2-3 Kumplis"`, `"4 Kumplis (or 2 with heroic appetites)"`)

#### Optional Metadata Fields

- **`gluten_free`** (boolean): Whether recipe is gluten-free
- **`spicy`** (string): Kumpli spice scale - creative freedom. Common values: `"None"`, `"Mild"`, `"Cheese Buldak"`, `"Buldak"`, `"2x Buldak"`
- **`good_for`** (array of strings): Use cases/occasions (e.g., `["comfort-food", "cooking-together", "emotional reset"]`)
- **`seasonality`** (string): Best season or `"anytime"`
- **`ingredient_access`** (string): Where to find ingredients (e.g., `"standard-eu"`, `"asian-store"`, `"standard-eu + asian-store"`)
- **`ingredient_count`** (integer or string): Total ingredients, can be a range (e.g., `18`, `"15-18"`)
- **`storage`** (string): Storage recommendations
- **`reheating`** (string): Reheating instructions
- **`pairing`** (string): Suggested sides or beverages
- **`tags`** (array of strings): Freeform descriptive tags (e.g., `["soul-warming", "boo-approved", "meaty"]`)

**Example:**
```json
"metadata": {
  "cuisine": "Mexican-inspired",
  "type": "Burrito",
  "gluten_free": false,
  "difficulty": "Medium",
  "spicy": "Buldak",
  "serves": "2-3 Kumplis",
  "good_for": ["comfort-food", "emotional reset", "cooking-together"],
  "seasonality": "anytime",
  "ingredient_access": "standard-eu",
  "ingredient_count": 18,
  "storage": "Best fresh; can be kept in fridge for up to 2 days",
  "reheating": "Oven (foil wrapped) at 180°C for 10–15 min",
  "pairing": "Lime soda, spicy pickled onions",
  "tags": ["soul-warming", "gerzemice-friendly", "boo-approved", "meaty"]
}
```

---

### `timing` (object, required)

Time requirements for the recipe.

- **`prep_minutes`** (integer, required): Preparation time in minutes
- **`total_minutes`** (integer, required): Total time including cooking in minutes

**Example:**
```json
"timing": {
  "prep_minutes": 30,
  "total_minutes": 45
}
```

---

### `ingredients` (array, required)

List of ingredients. Can be flat or grouped into sections.

#### Flat List (Simple Recipes)

Array of ingredient objects:

```json
"ingredients": [
  {
    "amount": "500g",
    "item": "mushrooms",
    "notes": "button or cremini"
  },
  {
    "amount": "3 cloves",
    "item": "garlic",
    "notes": "minced"
  },
  {
    "amount": "2 tbsp",
    "item": "butter"
  }
]
```

#### Grouped List (Complex Recipes)

Array of group objects with sub-items:

```json
"ingredients": [
  {
    "group": "🔥 Steak & Marinade",
    "items": [
      {
        "amount": "500-600g",
        "item": "flank steak"
      },
      {
        "amount": "2 tbsp",
        "item": "tomato paste"
      },
      {
        "amount": "1 tsp",
        "item": "smoked paprika"
      }
    ]
  },
  {
    "group": "🌾 Cilantro-Lime Rice",
    "items": [
      {
        "amount": "200g",
        "item": "cooked white rice",
        "notes": "about 1 cup"
      },
      {
        "amount": "1 tbsp",
        "item": "lime juice"
      }
    ]
  }
]
```

#### Ingredient Object Fields

- **`amount`** (string, optional): Quantity with unit (e.g., `"500g"`, `"2 tbsp"`, `"1 cup"`)
- **`item`** (string, required): Ingredient name
- **`notes`** (string, optional): Preparation notes, alternatives, or conversions

---

### `instructions` (array, required)

Ordered cooking steps. Instructions can be flat (simple recipes) or grouped (complex recipes with phases).

#### Simple Flat Format

Array of step objects:

```json
"instructions": [
  {
    "step": "Mix the tomato paste, paprika, chili, cumin, garlic, oil, lime juice, salt, and pepper. Rub onto steak and marinate 30 minutes to overnight."
  },
  {
    "step": "Mix warm cooked rice with lime juice, zest, cilantro, and salt."
  },
  {
    "step": "Heat a heavy pan with oil until hot. Pat steak dry slightly. Sear 1.5–2 minutes per side."
  }
]
```

#### Flat Format with Step Titles

Add optional `title` field for named steps:

```json
"instructions": [
  {
    "title": "Marinate the Steak",
    "step": "Mix the tomato paste, paprika, chili, cumin, garlic, oil, lime juice, salt, and pepper. Rub onto steak and marinate 30 minutes to overnight."
  },
  {
    "title": "Prepare Rice",
    "step": "Mix warm cooked rice with lime juice, zest, cilantro, and salt."
  },
  {
    "title": "Sear the Steak",
    "step": "Heat a heavy pan with oil until hot. Pat steak dry slightly. Sear 1.5–2 minutes per side. Let rest 5 minutes, then slice thinly against the grain."
  }
]
```

#### Grouped Format (Complex Recipes)

For recipes with multiple phases (prep → cook → assemble), use grouped instructions:

```json
"instructions": [
  {
    "group": "Prepare the Sauce",
    "steps": [
      {
        "step": "In a small bowl, mix gochujang, sesame oil, sugar, water, vinegar, soy sauce, and garlic."
      },
      {
        "step": "Add toasted sesame seeds if using. Stir until smooth and glossy."
      }
    ]
  },
  {
    "group": "Prep Vegetables",
    "steps": [
      {
        "title": "Spinach",
        "step": "Blanch briefly, drain, and season with a pinch of salt and sesame oil."
      },
      {
        "title": "Bean Sprouts",
        "step": "Blanch 2 minutes, then toss with salt and sesame oil."
      },
      {
        "title": "Carrot, Zucchini, Mushrooms",
        "step": "Sauté each separately in a touch of oil with salt. Keep them crisp-tender."
      }
    ]
  },
  {
    "group": "Assembly",
    "steps": [
      {
        "step": "Scoop warm rice into each wide bowl."
      },
      {
        "step": "Artfully arrange each topping in its own section around the bowl."
      },
      {
        "step": "Place the egg in the center and drizzle generously with gochujang sauce."
      }
    ]
  }
]
```

#### Substeps (Variants within a Step)

For variants or alternatives within a single step, use the `substeps` field:

```json
"instructions": [
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
        "step": "Add a tiny pinch of chili for a warm playful kick."
      }
    ]
  },
  {
    "title": "Assemble the mugs",
    "step": "Pour the hot chocolate into cups, add whipped cream, drizzle with caramel, and sprinkle a hint of salt for sparkle."
  }
]
```

**Substeps use the same `{title, step}` structure as regular steps.**

**Use substeps for:**
- Optional additions or flavor variations
- Serving suggestions
- Simple substitutions
- Alternative methods for the same step

**Don't use substeps for:**
- Distinct recipe phases (use `group` instead)
- Substantially different recipes (create separate recipe files)

---

#### When to Use Each Format

**Flat instructions:**
- Simple linear recipes (≤10 steps)
- No distinct phases or variants

**Grouped instructions:**
- Complex recipes with phases (prep → cook → assemble)
- Multiple components prepared separately
- Clear workflow stages

**Substeps:**
- Optional variants within a step
- Serving suggestions
- Simple substitutions
- Alternative flavorings

**Separate recipe files** (`recipe.{variant}.json`):
- Ingredients differ significantly (>30%)
- Cooking method substantially different
- Each version deserves own title/identity

---

#### Legacy: Small Variants as Final Group

Alternatively, for minor variations, you can add as a final instruction group:

```json
"instructions": [
  { "step": "..." },
  { "step": "..." },
  {
    "group": "Variations",
    "steps": [
      {
        "title": "For spicy version",
        "step": "Add 1 tsp chili flakes to the sauce."
      },
      {
        "title": "Vegetarian option",
        "step": "Replace meat with grilled tofu or tempeh."
      }
    ]
  }
]
```

**When to use grouped vs. flat:**
- **Flat**: Simple recipes with linear flow (≤10 steps)
- **Grouped**: Complex recipes with distinct phases, multiple components, or recipe variants

---

### `notes` (string, optional)

Additional recipe tips, variations, or Kumpli wisdom. Can alternatively be included in `story.md`.

**Example:**
```json
"notes": "Best enjoyed with a warm blanket and Miku purring nearby."
```

---

## Complete Example

```json
{
  "title": "Garlic Butter Mushrooms",
  "slug": "garlic-butter-mushrooms",
  "emoji": "🍄",
  "metadata": {
    "cuisine": "European",
    "type": "Side dish",
    "gluten_free": true,
    "difficulty": "Easy",
    "spicy": "None",
    "serves": "2 Kumplis",
    "good_for": ["quick", "vegetarian", "cozy"],
    "seasonality": "anytime",
    "ingredient_access": "standard-eu",
    "ingredient_count": 5,
    "storage": "Refrigerate up to 2 days",
    "reheating": "Reheat gently in pan",
    "pairing": "Crusty bread, grilled steak",
    "tags": ["quick", "vegetarian", "comfort-food"]
  },
  "timing": {
    "prep_minutes": 10,
    "total_minutes": 20
  },
  "ingredients": [
    {
      "amount": "300g",
      "item": "mushrooms",
      "notes": "button or cremini"
    },
    {
      "amount": "3 cloves",
      "item": "garlic",
      "notes": "minced"
    },
    {
      "amount": "3 tbsp",
      "item": "butter"
    },
    {
      "item": "salt and pepper",
      "notes": "to taste"
    },
    {
      "amount": "1 tbsp",
      "item": "fresh parsley",
      "notes": "chopped (optional)"
    }
  ],
  "instructions": [
    {
      "step": "Clean and slice mushrooms."
    },
    {
      "step": "Heat butter in a pan over medium heat."
    },
    {
      "step": "Add garlic and cook until fragrant (30 seconds)."
    },
    {
      "step": "Add mushrooms, cook 8-10 minutes until golden."
    },
    {
      "step": "Season with salt and pepper. Sprinkle with parsley if using."
    }
  ],
  "notes": "Don't crowd the pan - cook in batches if needed for best browning."
}
```

---

## `story.md` Format

The `story.md` file contains:
- **Background**: Emotional, mythical, or personal introduction to the recipe
- **Kumpli Notes**: Closing wisdom, serving suggestions, character notes
- **Images**: Embedded using standard Markdown syntax with captions

### Image References

Images are stored in the same recipe folder. Reference them with **filename only** (no path):

```markdown
![Alt text description](illustration-1.png)
*Optional italic caption below image*
```

### Example `story.md`

```markdown
# Background

Ciraf discovered this recipe on a misty autumn evening in the Allagan forest. The mushrooms glowed faintly in the twilight, and the garlic butter smell woke Miku from her nap under the moss-covered oak.

This is a dish of simplicity and warmth — no ceremony, just pure umami comfort.

![Glowing mushrooms in forest](illustration-1.png)
*Ciraf's mushroom gathering adventure*

## Kumpli Notes

Best enjoyed with a warm blanket and Miku purring nearby. Boo likes to eat this straight from the pan with crusty bread, standing by the stove like a small forest troll.

![Final dish on wooden table](photo-1.jpg)
*Our cozy Tuesday dinner*
```

---

## Tips for Recipe Creation

### With ChatGPT

1. **Phase 1**: Generate `recipe.json` with all structured data
2. **Phase 2**: Generate `story.md` with background and Kumpli notes
3. **Phase 3**: Generate/select images and add to folder with captions

### Manual Editing

- Edit `recipe.json` for recipe changes (ingredients, steps, metadata)
- Edit `story.md` for narrative changes (background, character notes)
- Keep images in same folder as recipe files
- Use descriptive image filenames (e.g., `illustration-steaming-pot.png`, `photo-final-plating.jpg`)

### Validation

Run optional validation (warnings only):
```bash
python scripts/validate_recipes.py recipes/recipe-slug/
```

---

## See Also

- `recipe.schema.json` - Full JSON Schema definition
- `reference/tags.json` - Suggested tag values
- `docs/migration-guide.md` - How to migrate old recipes
- `gpt-instructions/` - ChatGPT prompts for recipe creation


## Multi-Recipe Folders

### When to Use Multiple Recipes

A folder can contain multiple recipe files when:

1. **Substantial Variants**: Different versions with distinct ingredients or techniques (e.g., Korean vs. Classic burger)
2. **Regional Versions**: Same dish with regional adaptations
3. **Alternative Preparations**: Same concept, different execution methods

### Naming Convention

- **Primary recipe**: `recipe.json`
- **Variants**: `recipe.{variant-name}.json`

**Examples:**
```
recipes/seoul-smasher/
├── recipe.json           # Korean fusion version
├── recipe.classic.json   # Classic OG burger
└── story.md              # Shared narrative

recipes/okonomiyaki/
├── recipe.json           # Standard version
├── recipe.hiroshima.json # Hiroshima-style variant
└── story.md
```

### Renderer Behavior

- Discovers all `recipe*.json` files in folder
- Renders them in filename alphabetical order:
  1. `recipe.json` (always first)
  2. `recipe.classic.json`
  3. `recipe.spicy.json`
- All variants share the same `story.md`

### Alternative: Small Variants in Instructions

For **minor variations**, don't create separate recipe files. Instead:

**Option 1**: Add as final instruction group:
```json
{
  "group": "Variations",
  "steps": [
    {"title": "Spicy version", "step": "Add chili flakes..."},
    {"title": "Vegan option", "step": "Replace eggs with flax..."}
  ]
}
```

**Option 2**: Add as notes in specific steps:
```json
{
  "title": "Add cheese",
  "step": "Sprinkle cheddar on top. For extra spicy: mix in jalapeños."
}
```

**Use separate recipe files when:**
- Ingredients differ significantly (>30% different)
- Cooking method changes substantially
- Each version deserves its own title and identity

**Use inline variations when:**
- Simple substitutions (ingredient swaps)
- Optional additions (extra spice, garnishes)
- Serving suggestions

---


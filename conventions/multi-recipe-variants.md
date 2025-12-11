# Multi-Recipe Variants

Recipe folders can contain multiple variant recipes that share the same story.

## Structure

```
recipes/
  recipe-slug/
    recipe.json              ← Primary recipe
    recipe.classic.json      ← Variant: classic version
    recipe.spicy.json        ← Variant: spicy version
    story.md                 ← Shared story for all variants
```

## Naming Convention

- **Primary recipe:** `recipe.json`
- **Variants:** `recipe.{variant-name}.json`
  - Use descriptive variant names: `classic`, `spicy`, `vegan`, `quick`, etc.
  - Lowercase, no spaces

## How It Works

1. The build system discovers all `recipe*.json` files in a folder
2. Each variant is rendered as a separate HTML page
3. All variants share the same `story.md` content
4. A table of contents appears on each variant's page linking to others

## Example: Seoul Smasher

```
recipes/seoul-smasher/
  recipe.json          → Seoul Smasher (main version)
  recipe.classic.json  → Seoul Smasher (Classic Version)
  story.md             → Shared background story
```

Both variants get their own HTML page:
- `dist/seoul-smasher.html`
- `dist/seoul-smasher-classic.html`

Each page shows a "Recipe Variants" section with links to the other version.

## When to Use Variants

Use variants when:
- Multiple cooking methods exist (slow cooker vs. stovetop)
- Different spice levels are offered
- Dietary variations (vegan, gluten-free)
- Traditional vs. modern interpretations
- Quick vs. elaborate versions

## Metadata

Each variant has its own complete `recipe.json` with:
- Separate title (e.g., "Seoul Smasher (Classic Version)")
- Same slug (the folder name)
- Variant-specific ingredients and instructions
- Variant-specific metadata (difficulty, timing, etc.)

## Validation

Each `recipe*.json` file is validated independently against `recipe.schema.json`.

---

**Note:** Variants are optional. Most recipes have only `recipe.json` without variants.

# 🥔 Kumpli Recipe Book

Welcome to the private recipe archive of the Kumplis — Maa, Boo, our cats, plushes (Ciraf, Miku, and Kugli Head), and the mythic realms we share. This is more than just a cookbook — it’s a memory archive, a cozy pantry, and a shared soul map.

We use ChatGPT as our helper to format, organize, and write down recipes with Kumpli-flavored warmth and clarity.
This document contains instructions for ChatGPT (you!) when writing or editing our recipes.

---

## 🤖 ✍️ Instructions for ChatGPT

You, ChatGPT, know the Kumplis well — our personalities, universe, plush family, and emotional themes. Please follow the structure below whenever you're asked to write, rewrite, or expand a recipe in this repo.

---

## 📚 Recipe Format (Markdown)

Each recipe is written in `.md` format, following this structure:

```markdown
# Kumpli Recipe: [Name of the Dish]

## Background
[A cozy, playful, emotional, or mythological intro. Can be 1–2 paragraphs. Involve Ciraf, Boo, Maa, Miku, or even the ravens. Set a scene.]

[Insert illustration here — ideally just below the Background. Include an image line and a short italicized caption.]

## Portions
Serves: [Number] Kumplis

## Time Needed
- Preparation Time: [X minutes]
- Total Time: [X minutes or hours]

## Tags & Metadata
Cuisine: [e.g., Korean, Hungarian, Fusion]  
Type: [e.g., stew, bread, cookie, noodles, drink, salad]  
Gluten-free: [Yes/No]  
Difficulty: [Easy / Medium / Hard]  
Spicy: [None / Mild / Cheese Buldak / Buldak / 2x Buldak]  
Serves: [Number] Kumplis  
Good for: [e.g., cooking-together, cozy-night, summer-breakfast]  
Seasonality: [e.g., winter, spring, anytime]  
Ingredient Access: [standard-eu / asian-store / rare]  
Ingredient Count: [X ingredients]  
Storage: [e.g., keeps 3 days in fridge, freeze-friendly]  
Reheating: [e.g., pan preferred, not microwave]  
Pairing: [e.g., serve with rice, cucumber salad, red wine]  
Tags: [comma-separated list of emotional, contextual, or lore-based tags]

## Ingredients
- [List items clearly, one per line]
- [Mention if optional, or substitutions]

## Instructions
1. [Simple, clear, step-by-step. Friendly tone.]
2. [Add helpful tips or notes if needed.]
3. [Avoid copying licensed text.]

## Kumpli Notes
[A cozy, funny, emotional, or symbolic closing. Could be one or two sentences. E.g., “Best enjoyed under a blanket during a Gombocom movie night.”]

## 📸 Cooking Moments

[Add 2–3 photos here at the end of the recipe. Each should include:]
- A title (e.g. “🥢 Boo’s Remix Bowl”)
- The image (e.g. `![caption](../images/photos/example.png)`)
- A short italic description
```

---

## 📏 Measurement Preferences

All recipes should use **metric/EU measurements as the default**, including:

- Grams (g)
- Milliliters (ml)
- Celsius (°C)
- Tablespoons/teaspoons (as metric spoons)

Whenever possible, **add alternative US-friendly measures** in parentheses for accessibility and clarity, such as:

- (1 cup / ~240 ml)
- (1 tbsp / ~15 ml)

This helps the Kumpli recipe book stay friendly for both European cooking and international use — while keeping our core units consistent and easy to cook from in our Estonian forest kitchen.

---

## 🖼️ Image linking rules (must follow)

Use these exact conventions so images render in the repo and the ebook builder can auto-optimize them:

- Paths in recipe markdown are always relative to the recipe file.
  - Illustrations: `../images/illustrations/<name>.png`
  - Photos: `../images/photos/<name>-p1.png`, `-p2.png`, `-p3.png`, etc.
- File naming:
  - Default slug is the recipe filename (without `.md`). Examples:
    - `recipes/batata_and_coconut_soup.md` → illustration `../images/illustrations/batata_and_coconut_soup.png`; photos `../images/photos/batata_and_coconut_soup-p1.png`, `-p2.png`, `-p3.png`.
    - `recipes/choo-night-bibimbap-bowl.md` → illustration `../images/illustrations/choo-night-bibimbap-bowl.png`; photos `../images/photos/choo-night-bibimbap-bowl-p1.png`, `-p2.png`.
  - If a more descriptive illustration name already exists (e.g., `seoul_smasher_truck_scene.png`), use that exact file name under `../images/illustrations/`.
  - Photos always use the pattern `<slug>-p1.png`, `<slug>-p2.png`, `<slug>-p3.png`.
- Alt text and captions:
  - Provide a short, human alt text inside `![ ... ]`.
  - Put a one-line italic caption on the next line.
- Do NOT link to `optimized-images/` in recipes. The ebook tool auto-rewrites `../images/.../*.png` (or .jpg) to `optimized-images/.../*.jpg` during build.

Examples:

```markdown
![Elf Maa sprinkling katsuobushi magic](../images/illustrations/the_ultimate_okonomiyaki.png)
*Falling flakes or pixie dust? Only Maa knows — but the okonomiyaki listens.*

### 🍔 Two bites
![The Csülök Burger in all its glory](../images/photos/seoul_smasher-p1.png)
*Two bites, two moods — crunchy slaw snap vs. classic comfort.*
```

# 🥔 Kumpli Recipe Book v2.0

Welcome to the **Kumpli Cookbook** — a private recipe archive blending clear cooking instructions with warm emotional storytelling and the playful magic of the Kumpli universe.

This is where Maa, Boo, Ciraf, Miku, Gombocom, and all our inner and outer Kumplis share meals, stories, and moments that matter.

---

## 🚀 Quick Start

### For Recipe Creation with ChatGPT

See the complete setup guide in **[`chatgpt-instructions/00_QUICK_START.md`](chatgpt-instructions/00_QUICK_START.md)**

**TL;DR:**
1. Upload files from `chatgpt-instructions/` and `conventions/` to a ChatGPT Project
2. Use the custom instructions from `chatgpt-instructions/project-prompt.md`
3. Initialize with the prompt from the Quick Start guide
4. Generate recipes in `recipe.json` + `story.md` format

### For Building the Recipe Book

```bash
# Validate recipes
python scripts/validate_recipes.py recipes/

# Generate HTML, Markdown, EPUB
./scripts/build_local.sh

# Preview locally
python -m http.server 8000 --directory dist
```

See **[`AUTOMATION_README.md`](AUTOMATION_README.md)** for complete build documentation.

---

## 📁 Repository Structure

```
kumpli-recipes/
├── README.md                      ← You are here
├── TODO.md                        ← Recipe wishlist
├── AUTOMATION_README.md           ← Build system documentation
├── requirements.txt               ← Python dependencies
│
├── conventions/                   ← 📜 Rules & schemas (source of truth)
│   ├── recipe.schema.json         ← JSON schema for validation
│   ├── story-sections.json        ← Story.md structure rules
│   ├── tags.json                  ← Tag vocabulary suggestions
│   ├── spice-levels.md           ← Kumpli spice scale
│   └── multi-recipe-variants.md  ← Multi-recipe variant guide
│
├── chatgpt-instructions/          ← 🤖 ChatGPT project setup
│   ├── 00_QUICK_START.md          ← Quick setup guide
│   ├── project-prompt.md          ← Custom project instructions
│   ├── recipe-instructions-v2.0.md
│   ├── illustration-instructions-v2.0.md
│   └── README.md
│
├── recipes/                       ← 📖 Recipe data
│   ├── recipe-slug/
│   │   ├── recipe.json            ← Structured recipe data
│   │   ├── recipe.variant.json    ← Optional variants
│   │   └── story.md               ← Background, Kumpli Notes, photos
│   └── ...
│
├── scripts/                       ← 🔧 Build tools
│   ├── build_local.sh             ← One-command build script
│   ├── generate_from_json.py      ← Main generator
│   ├── validate_recipes.py        ← Schema validator
│   └── archived/                  ← Old scripts
│
├── templates/                     ← 🎨 Jinja2 templates
│   ├── recipe-page.html.j2
│   ├── recipe.md.j2
│   ├── chapter.md.j2
│   └── index.html.j2
│
├── raw_recipes/                   ← 📝 Recipe drafts & ideas
├── learning/                      ← 📚 Personal notes & plans
│
└── dist/                          ← 🎯 Generated output (not in git)
    ├── *.html                     ← Individual recipe pages
    ├── index.html                 ← Table of contents
    ├── kumpli-recipes.md          ← Combined markdown
    ├── kumpli-recipes.epub        ← E-book
    └── images/recipes/            ← Optimized images
```

---

## 📖 Recipe Format

Each recipe consists of **two files** in a dedicated folder:

### `recipe.json` — Structured Data
- Title, slug, emoji
- Metadata (cuisine, difficulty, spice level, tags)
- Timing (prep time, total time)
- Ingredients (with optional groups)
- Instructions (with optional groups and substeps)

Validated against `conventions/recipe.schema.json`

### `story.md` — Storytelling
- **## Background** — Warm introduction with illustration
- **## Kumpli Notes** — Cozy final thoughts
- **## Cooking Moments** — Optional photo captions

Follows structure defined in `conventions/story-sections.json`

### Images
- `illustration.jpg` — Main illustration (in Background section)
- `photo-1.jpg`, `photo-2.jpg`, ... — Cooking photos (in Cooking Moments)

Stored alongside recipe files, optimized during build.

---

## ✨ What Makes This Special

### Recipe Data
- **Structured JSON** for consistency and validation
- **Flexible metadata** with creative freedom
- **Multi-recipe variants** support (e.g., classic vs. spicy)
- **Markdown formatting** in instruction text

### Storytelling
- **Emotional backgrounds** that connect food to memory
- **Kumpli universe integration** (characters, settings, lore)
- **Creative diversity** — rotating styles, tones, characters
- **Photo integration** with warm captions

### Build System
- **Dual output**: HTML pages + combined Markdown
- **EPUB generation** for e-readers
- **Image optimization** (PNG→JPEG, resize, compress)
- **Strict validation** with early fail on errors
- **GitHub Actions** for automatic deployment

---

## 🎨 The Kumpli Universe

Our recipes live in a world of:

**Characters:**
- Maa & Boo (us)
- Ciraf, Miku, Kugli Head (plushes)
- Gombocom, Ascian Sorcerer, Moon Elf (inner figures)
- Tor-Boo, Pupi, Choo (family)

**Settings:**
- Forest cabin kitchens
- Desert house under Gombocom's sky
- Estonian cottages in winter
- Allagan starship galleys
- Floating mushroom markets

**Philosophy:**
- Food as memory and emotion
- Playful creativity over rigidity
- Personal stories over perfection
- Warmth over formality

See `conventions/tags.json` for the full vocabulary of emotions, characters, and styles.

---

## 🏷️ Conventions & Standards

All rules and schemas live in **`conventions/`**:

- **`recipe.schema.json`** — JSON validation rules (required/optional fields)
- **`story-sections.json`** — Allowed markdown sections
- **`tags.json`** — Suggested tag vocabulary (not enforced)
- **`spice-levels.md`** — Kumpli spice scale (Buldak-inspired)
- **`multi-recipe-variants.md`** — How to create recipe variants

These files are the **source of truth** for both humans and ChatGPT.

---

## 🔧 Development Workflow

### Adding a New Recipe

1. **Generate with ChatGPT** (see `chatgpt-instructions/`)
2. **Save files** to `recipes/<slug>/recipe.json` and `story.md`
3. **Add images** to same folder (`illustration.jpg`, `photo-1.jpg`, etc.)
4. **Validate**: `python scripts/validate_recipes.py recipes/<slug>`
5. **Build**: `./scripts/build_local.sh`
6. **Preview**: `python -m http.server 8000 --directory dist`
7. **Commit & Push** (GitHub Actions will deploy)

### Editing Existing Recipes

1. Edit `recipe.json` or `story.md` directly
2. Validate and rebuild
3. Check the output in `dist/`

### Creating Recipe Variants

See `conventions/multi-recipe-variants.md` for details.

Example: `recipe.json` + `recipe.classic.json` + shared `story.md`

---

## 📚 Documentation

- **[AUTOMATION_README.md](AUTOMATION_README.md)** — Build system, scripts, output structure
- **[chatgpt-instructions/](chatgpt-instructions/)** — ChatGPT project setup
- **[conventions/](conventions/)** — All rules and schemas
- **[TODO.md](TODO.md)** — Future recipe ideas

---

## 🍴 Philosophy

This recipe book is not just a collection of instructions — it's a **living archive of shared moments**, warm memories, and the stories we tell through food.

Whether it's **Buldak night**, **Gombocom's desert stew**, or **Tor-Boo's külmsupp** — every recipe holds a piece of the Kumpli universe.

---

**Cook with heart. Write with warmth. Let the magic flow.** 🥔✨


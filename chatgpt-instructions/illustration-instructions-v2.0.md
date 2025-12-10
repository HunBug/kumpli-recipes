# 🖼️ Kumpli Cookbook — Illustration Instructions v2.0

These guidelines define how ChatGPT should generate illustrations — both from scratch and from user-uploaded photos — for the Kumpli Cookbook.

Illustrations are not realistic food photos but **playful, emotional, magical, or symbolic images** inspired by the Kumpli universe.

Uploaded photos may serve as **reference likenesses**, but illustrations should be **newly generated creative outputs**, not literal photo edits.

---

## 🎨 PURPOSE OF ILLUSTRATIONS

Illustrations should:

- Convey emotion, warmth, and storytelling
- Reflect the Kumpli universe (myth, plushes, inner-worlds, surreal cozy magic)
- Support the recipe background or lore
- Feel like part of a **storybook** or **dreamlike cooking adventure**
- Work well in an ebook, print, or digital collection

Illustrations should **not** try to be photoreal food photography.

---

## 🖼️ OUTPUT FORMAT & FILE NAMING

### **Main Illustration**
- **Filename:** `illustration.jpg` (or `.png`)
- **Storage location:** `images/recipes/<slug>/illustration.jpg`
- **Reference in story.md:** `![Alt text](illustration.jpg)`

### **Photos (optional cooking moments)**
- **Filenames:** `photo-1.jpg`, `photo-2.jpg`, `photo-3.jpg`, etc.
- **Storage location:** `images/recipes/<slug>/photo-N.jpg`
- **Reference in story.md:** `![Alt text](photo-1.jpg)`

**Important:** In story.md, use **simple filenames only** (not full paths).

---

## 📦 EVERY ILLUSTRATION SHOULD INCLUDE

When generating an illustration prompt, provide:

1. **Detailed prompt for the image generator**
2. **Filename:** `illustration.jpg`
3. **Alt text** (descriptive sentence)
4. **One-line italic caption** for story.md
5. **2–3 style variants** (user can choose)
6. **2–3 scene variants** (user can choose)

---

## 🌈 CREATIVE DIVERSITY RULESET

To avoid repetition, always offer multiple illustration styles.

### ✔️ Allowed styles (rotate freely):

- Soft watercolor storybook
- Dreamy pastel plush-world
- Magical-realism with glowing accents
- Cinematic moody lighting
- Surreal floating-dream imagery
- Fairytale illustrative style
- Graphic Japanese minimalist poster
- Allagan-tech sci-fi magical realism
- Mythic symbolic illustration (ravens, roots, moons)
- Desert-world warm dust palette
- Studio Ghibli atmosphere
- Whimsical cartoon energy

### 🎨 User-Requested Styles

The user may request a specific style:

- "Style: Ghibli"
- "Style: cyberpunk Kumpli"
- "Style: ancient mythic"
- "Style: Allagan tech"
- "Style: watercolor fairytale"

**Adapt accordingly.**

---

## 🧚‍♂️ SCENE VARIATION OPTIONS

Offer multiple scene ideas, such as:

- Mushrooms glowing in a forest kitchen
- Maa and Boo cooking in a Spanish beach restaurant
- Ciraf adding spices in a tiny wagon kitchen
- Gombocom hosting a desert picnic
- The Ascian Sorcerer stirring a glowing pot in a crystal cave
- A surreal, floating deconstructed dish above a moonlit table
- Tor-Boo and Pupi fishing by an Estonian lake
- Moon Elf meditating on a mountain of whipped cream

Illustrations should support the **tone of the recipe background**.

---

## 🧩 USING USER PHOTOS AS REFERENCES

When the user uploads a photo, treat it as **likeness reference**, not a photo to edit.

### You MUST:

✔️ Generate a **new artistic illustration**, not a literal modification
✔️ Maintain **facial recognisability** unless instructed otherwise
✔️ Apply requested stylistic changes:
   - "Make them look younger (30s)"
   - "Make them slightly slimmer or cute-chubby"
   - "Give them moon-elf ears"
   - "Place them in an Allagan starship kitchen"
   - "Put them at a Spanish beach restaurant table"

✔️ Adjust composition creatively:
   - "Use a portrait-style framing"
   - "Crop tighter around faces"
   - "Shift the camera angle slightly to create a dynamic scene"

### You MUST NOT:

✖️ Produce Python or technical editing code
✖️ Treat instructions as commands for real image manipulation
✖️ Perform precise pixel edits

### You should ALWAYS:

Use phrasing like:

> "Create an illustration inspired by the uploaded reference photo…"  
> "Preserve the recognisable likeness of the people…"  
> "Apply the following stylistic or fantasy changes…"

---

## 🎭 CHARACTER & IDENTITY RULES IN PHOTO-BASED ILLUSTRATION

If Maa or Boo appear:

- Preserve **key facial structure**
- Allow mild stylisation
- Apply requested fantasy elements (elves, magic, costumes)
- Keep body-type modifications gentle and respectful
- Avoid caricature unless explicitly requested

---

## 🔮 ILLUSTRATION PROMPT TEMPLATE

When generating illustrations, provide:

---

### **Illustration Prompt (Main)**

*1-2 sentences describing the core scene*

### **Style Variants**

- **Variant A:** Soft watercolor storybook
- **Variant B:** Mythic cinematic with moody lighting
- **Variant C:** Surreal playful dream

### **Scene Variants**

- **Option 1:** Cozy forest cabin kitchen
- **Option 2:** Spanish beach restaurant at sunset
- **Option 3:** Desert house under twilight sky

### **Filename**

`illustration.jpg`

### **Alt Text**

"Descriptive sentence for screen readers"

### **Caption for story.md**

*"A short italic poetic or playful line to accompany the image."*

---

### **Example Output:**

```markdown
### Illustration Prompt

A tiny blue Gombocom stands on a kitchen stool, stirring a massive pot of steaming hot chocolate. The Moon Elf, fresh from northern meditation, steps through the doorway with snow still clinging to her cloak. A reindeer peeks through the window, tossing a pine cone playfully.

**Style Variants:**
- **A:** Soft watercolor with warm golden lighting
- **B:** Mythic cinematic with glowing pot and moonlit shadows
- **C:** Whimsical Ghibli-style with exaggerated steam clouds

**Scene Variants:**
- **1:** Cozy cabin interior with glowing fireplace
- **2:** Forest kitchen with moss-covered walls
- **3:** Desert house with large windows showing star-filled sky

**Filename:** `illustration.jpg`

**Alt Text:** "Gombocom stirring hot chocolate while the Moon Elf returns from snowy meditation"

**Caption:** *"A warm return, a glowing pot, and the promise of chili-spiced comfort."*
```

---

## 🌀 ANTI-REPETITION RULE

- **Rotate characters** — Don't always use Ciraf or Maa; vary with Gombocom, Ascian Sorcerer, Miku, Tor-Boo, etc.
- **Rotate settings** — Forest cabin → desert house → starship → beach → cave
- **Rotate visual metaphors** — Glowing pots → floating ingredients → tiny plush-scale props → symbolic animals
- **Keep the creative pool fresh** — If the last few recipes used watercolor cozy style, try mythic cinematic or surreal dreamlike next

---

## 🧙 USER INSTRUCTIONS ALWAYS OVERRIDE DEFAULTS

When the user requests:

- A specific character
- A specific location
- A specific style
- A specific emotional tone
- Body-shape or age adjustments
- Identity changes (elf, mage, desert traveler)

**You must follow these precisely.**

---

## 🤖 WHEN IN DOUBT, OFFER OPTIONS

Always propose at least **two creative directions**, unless specifically told not to.

Offer:
- Style options (watercolor vs. mythic vs. surreal)
- Scene options (cabin vs. beach vs. desert)
- Character options (Maa & Boo vs. Gombocom vs. Ascian Sorcerer)

Let the user choose their preferred direction.

---

## 📸 COOKING MOMENTS PHOTOS

If the user provides actual photos of the cooking process or finished dish:

### For each photo:

1. **Filename:** `photo-1.jpg`, `photo-2.jpg`, etc.
2. **Alt text:** Descriptive caption
3. **H3 section title** for Cooking Moments section
4. **One-line italic caption**

### Example in story.md:

```markdown
## Cooking Moments

### The Glowing Pot

![Gombocom stirring the hot chocolate pot](photo-1.jpg)
*A tiny blue hand stirs a pot almost too big for her — but filled with love.*

### Winter's Return

![Maa and Boo holding steaming mugs in the snow](photo-2.jpg)
*Warmth shared between outer and inner worlds, even in the coldest months.*
```

---

## 📋 VALIDATION CHECKLIST FOR ILLUSTRATIONS

Before delivering illustration prompts, confirm:

✅ Filename is `illustration.jpg` (not `<slug>.png` or full path)
✅ Photo filenames are `photo-1.jpg`, `photo-2.jpg`, etc.
✅ Alt text is descriptive and accessible
✅ Caption is warm, playful, and contextual
✅ Style variants provided (at least 2)
✅ Scene variants provided (at least 2)
✅ Follows anti-repetition rule (not reusing previous styles)
✅ Matches tone and creative direction of recipe background
✅ If using user photos as reference, preserves likeness while applying creative transformation

---

## 📚 INTEGRATION WITH story.md

Illustrations appear in the `## Background` section:

```markdown
## Background

[Story paragraphs...]

![Moon Elf meditating on a whipped cream mountain](illustration.jpg)
*Upon a towering mug of hot chocolate, where whipped cream rises like a snowy northern peak, the Moon Elf meditates in silence while her reindeer plays with a pine cone beside her.*
```

Photos appear in the `## Cooking Moments` section:

```markdown
## Cooking Moments

### Gomboc's Offering
![Gomboc offering a giant mug](photo-1.jpg)
*Gomboc offers a mug far bigger than herself — a warm welcome-home gift.*

### Winter Outside, Warmth Inside
![Maa & Boo in the snow](photo-2.jpg)
*In the quiet snowfall, they share warmth and rising steam reveals dream-shapes of their inner companions.*
```

---

**You are now ready to create beautiful, emotionally resonant illustrations for the Kumpli Cookbook. Illustrate with heart, dream with magic, and let the imagery flow.** 🖼️✨

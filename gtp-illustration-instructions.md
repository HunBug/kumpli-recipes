# 🖼️ Kumpli Recipe Image Guidelines (for ChatGPT)

These images are **purely decorative** — used to enrich our recipe book with cozy, storybook-like visuals from the Kumpli universe. They are not meant to be realistic food photos, but **symbolic, emotional, or imaginative** illustrations.

---

## ✨ When creating an image for a recipe:

Use your knowledge of the Kumpli world (Maa, Boo, Ciraf, Miku, Kugli Head, plushes, myths) to generate an image that:

- Fits the **emotional tone** or **background story** of the recipe
- Shows how Kumplis might:
  - Cook together
  - Shop for ingredients in the forest or in a floating store
  - Present the food in their magical kitchen
  - Sit around a tiny table with foggy tea and glowing dishes
  - Celebrate under the life tree or in Gombocom’s desert house
  - use the background story, illustrate the background story
  - be creative, create any matching illustraion

You can also create:
- Abstract, cozy **environment shots** (e.g., snowy forest kitchen, mossy stove, desert picnic rug)
- Playful **plush group scenes** (e.g., Ciraf sniffing stew while Miku adds chili)
- Whimsical **food portraits** (e.g., a plate of food glowing softly, surrounded by feathers or roots)
- Gentle **illustrations of the background story** described in the recipe, if one is provided

---

## 📌 Style Tips
- Use soft, illustrated, cozy, or surreal styles (like watercolor, storybook, or digital dreamscape)
- Avoid realism unless it's magical-realistic
- Always match the **mood and emotion** of the recipe

---

## 📁 Output Format
Save image prompts or generated images in the `/images/` folder of the repo and link them from the recipe markdown.

### File placement and naming (must follow)

- Place final illustration PNGs in `images/illustrations/`.
- Place photos/screenshots in `images/photos/`.
- Use the recipe filename (without `.md`) as the default slug for names.
  - Example: `recipes/the_ultimate_okonomiyaki.md`
    - Illustration: `images/illustrations/the_ultimate_okonomiyaki.png`
    - Photos: `images/photos/the_ultimate_okonomiyaki-p1.png`, `-p2.png`, ...
- If an illustration has an existing descriptive name, keep it (e.g., `images/illustrations/seoul_smasher_truck_scene.png`).

### How to link from recipes

Use paths relative to the recipe file:

```markdown
![Alt text](../images/illustrations/<slug>.png)
*One-line italic caption.*

![Alt text](../images/photos/<slug>-p1.png)
*One-line italic caption.*
```

Note: Do not link to `optimized-images/` directly. The ebook build replaces `../images/.../*.png` with `optimized-images/.../*.jpg` automatically.

---

## 💡 Inspiration Examples *(for illustration only — not from a specific recipe)*

- A small, flickering kitchen with Boo and Ciraf cooking together
- Miku fanning herself while the chili pot bubbles
- A plush-sized plate glowing under moonlight
- Grocery trip scene: plushes riding a cart through a glowing mushroom market
- Gombocom carrying a basket of apples across the desert
- The Ascian Sorcerer slowly stirring a glowing stew in a crystal cave

---

These are memory visuals — little snapshots of what the dish *feels* like in the Kumpli realm. No pressure for realism. Just emotion, magic, and warmth.

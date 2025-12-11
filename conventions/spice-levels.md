# Kumpli Spice Levels

The Kumpli Cookbook uses a playful, personal spice scale inspired by Korean Buldak (fire chicken) ramen heat levels.

## Standard Levels

- **None** — No heat at all
- **Mild** — Gentle warmth, family-friendly
- **Cheese Buldak** — Moderate heat with creamy balance
- **Buldak** — Serious fire chicken heat
- **2x Buldak** — Extreme spice, for the brave

## Usage

The `spice_level` field in `recipe.json` accepts these values but is **not strictly enforced**. Feel free to use:
- Creative variations: `"Mild-to-Cheese-Buldak"`, `"Buldak territory"`
- Custom descriptions: `"Gentle heat"`, `"Heroic spice level"`
- Mixed styles: `"None (rum version), Mild (chili version)"`

## In Metadata

```json
"metadata": {
  "spice_level": "Cheese Buldak"
}
```

This field is **optional**. If omitted, assume no significant spice level.

---

**Philosophy:** Spice levels should feel playful and personal, not clinical. The Kumpli way embraces both precision and creative freedom.

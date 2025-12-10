# Plan: Kumpli Cookbook Repository Refactoring

Restructure the recipe repository from tightly-coupled Markdown files to a flexible architecture with separated content (JSON data), narrative (Markdown stories), and presentation (Jinja2 templates). This enables easier editing, multiple output formats, and maintains the creative Kumpli storytelling workflow.

## Steps

### Phase 1: Design & Documentation (Foundation)

1. **Design JSON schema and reference documentation** — Define `recipe.schema.json` with all metadata fields (cuisine, difficulty, spicy, timing, ingredients, steps). Create `docs/recipe-format-reference.md` documenting the JSON structure with examples. Add `reference/tags.json` listing valid tag values (for ChatGPT reference only). Create `scripts/validate_recipes.py` using `jsonschema` library for warnings only (non-blocking, creativity first).

2. **Create helper tools for manual migration** — Build `scripts/recipe_template_generator.py` to scaffold new recipe folders with empty `recipe.json` and `story.md` templates. Create `docs/migration-guide.md` with step-by-step manual migration instructions.

### Phase 2: Content Migration (Manual Work)

3. **Migrate all recipes manually** — For each recipe in `recipes/`:
   - Create `recipes/<slug>/` folder
   - Extract metadata → `recipe.json`
   - Extract background/Kumpli notes → `story.md` 
   - Move images from `images/illustrations/` and `images/photos/` → `recipes/<slug>/`
   - Delete old `.md` file from `recipes/`
## Decisions Made

1. **Template approach**: Single template/output format initially. Device-specific variants deferred to future.
2. **Character database**: Skipped for now. Can be added later by creative team if needed.
3. **EPUB generation**: **TBD - Low priority**. Focus on HTML/GitHub Pages first. Will revisit EPUB approach later (Pandoc vs native Python libraries).
4. **Execution**: Sequential phases. Phase 2 (manual migration) will be done with assistance.

## Implementation Notes

- **Clean Break**: Old recipe `.md` files will be deleted after migration. No dual-format support.
- **Broken Build During Migration**: Build system will be broken while recipes are being migrated. This is acceptable.
- **Manual Migration Only**: No automated parsing scripts. Human judgment for all content extraction.
- **Validation as Safety Net**: `validate_recipes.py` produces warnings only, never blocks. Creativity takes priority over rules.
- **Image Paths**: Simple filename references (e.g., `illustration-1.png`) in story.md, images live in same recipe folder.
- **Fix-as-you-go**: After build scripts updated, fix any issues iteratively in recipes and/or scripts until everything works.
   - Renders via Jinja2 templates
   - Handles image paths (relative to recipe folder)
   - Outputs to `dist/` directory
   - Update `scripts/optimize_images.py` to scan `recipes/*/` for images
   - Update `requirements.txt`: add `Jinja2`, `jsonschema`

7. **Update CI/CD workflow** — Modify `.github/workflows/build-and-deploy.yml`:
   - Call new build scripts
   - Add optional validation step (warnings only)
   - Keep deployment logic to HunBug.github.io

### Phase 4: Documentation Update

8. **Update ChatGPT instruction files for new workflow** — Restructure `gpt-instructions.md` or split into:
   - `gpt-instructions/01-recipe-json.md` (how to generate recipe.json)
   - `gpt-instructions/02-story-generation.md` (how to write story.md with image references)
   - `gpt-instructions/03-illustrations.md` (image generation/captioning)
   - Update with new file structure and image path conventions (filename only, same folder)

9. **Update repository documentation** — Update `README.md` with new workflow, folder structure, and migration status. Update `AUTOMATION_README.md` if it references old structure.

6. **Update ChatGPT instruction files for new workflow** — Split current `gpt-instructions.md` into `gpt-instructions/01-recipe-json.md` (generate recipe.json), `gpt-instructions/02-story-generation.md` (generate story.md with flexible image references), `gpt-instructions/03-illustrations.md` (image generation/captioning). Update README.md with new workflow documentation.

## Further Considerations

1. **Migration validation strategy?** — Should we generate outputs from both old and new systems in parallel during transition, then diff the HTML/EPUB to ensure equivalence? Or accept minor formatting differences?

2. **Template customization for different devices?** — You mentioned wanting separate HTML per device later. Should we plan template structure now to support `templates/mobile/`, `templates/desktop/`, `templates/print/` variants? Or defer until after basic refactoring?

3. **Character database integration?** — The Kumpli universe has rich lore (Maa, Boo, Ciraf, Gombocom, etc.). A `reference/characters.json` could be maintained by the "creative team" for ChatGPT reference, but kept separate from the build system. Should we create a placeholder structure for this, or leave it entirely to manual creative process?

## Implementation Notes

- **Gradual Migration**: Both old (`.md` files) and new (folder-based) recipes can coexist during transition. Build scripts will support both formats.
- **No Automated Parsing**: Human judgment preserved for unique formatting, creative elements, and special recipe variations.
- **Reference Files**: `reference/tags.json` and potential `reference/characters.json` are documentation aids for ChatGPT, not validation constraints.
- **Creative Flexibility**: Story.md format remains freeform Markdown with no structural restrictions beyond image embedding conventions.

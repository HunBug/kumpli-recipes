#!/usr/bin/env python3
import os
import argparse
from typing import Set, Dict, Any
from PIL import Image, ImageOps


def optimize_image(
    input_path: str,
    output_path: str,
    quality: int = 85,
    max_width: int = 1200,
) -> bool:
    """Optimize a single image"""
    try:
        with Image.open(input_path) as img:
            # Honor EXIF orientation
            img = ImageOps.exif_transpose(img)

            # Convert RGBA/LA to RGB if necessary
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Resize if too wide
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize(
                    (max_width, new_height),
                    Image.Resampling.LANCZOS,
                )

            # Save optimized image
            out_dir = os.path.dirname(output_path)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
            icc = img.info.get("icc_profile")
            save_kwargs: Dict[str, Any] = {
                "quality": quality,
                "optimize": True,
                "progressive": True,
            }
            if icc:
                save_kwargs["icc_profile"] = icc
            # Rely on output_path extension for format
            img.save(output_path, **save_kwargs)

            return True
    except Exception as e:
        print(f"Error optimizing {input_path}: {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize images for web and e-book",
    )
    parser.add_argument(
        "--input-dir",
        default="images",
        help="Input directory (default: images)",
    )
    parser.add_argument(
        "--output-dir",
        default="optimized-images",
        help="Output directory",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="JPEG quality (1-100)",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1200,
        help="Maximum width in pixels",
    )

    args = parser.parse_args()

    # Typed locals for linters
    input_dir: str = args.input_dir
    output_dir: str = args.output_dir
    quality: int = int(args.quality)
    max_width: int = int(args.max_width)

    # Exclude folders from traversal
    exclude_dirs: Set[str] = {
        output_dir,
        "dist",
        ".git",
        ".github",
        "scripts",
        "__pycache__",
    }

    optimized_count = 0
    for root, dirs, files in os.walk(input_dir):
        # mutate dirs in-place to prevent walking into excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                input_path = os.path.join(root, file)
                rel_path = os.path.relpath(input_path, input_dir)

                # Change extension to .jpg for optimized version
                name, _ = os.path.splitext(rel_path)
                output_path = os.path.join(output_dir, name + ".jpg")

                # Skip if up-to-date
                try:
                    if os.path.exists(output_path):
                        src_mtime = os.path.getmtime(input_path)
                        out_mtime = os.path.getmtime(output_path)
                        if out_mtime >= src_mtime:
                            # Up-to-date; skip
                            continue
                except OSError:
                    pass

                if optimize_image(input_path, output_path, quality, max_width):
                    optimized_count += 1
                    print(f"Optimized: {rel_path}")

    print(f"Optimized {optimized_count} images")


if __name__ == "__main__":
    main()

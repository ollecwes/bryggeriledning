from PIL import Image
import os
import sys
import argparse
from pathlib import Path

def optimize_image(input_path, output_path_png, output_path_webp):
    """
    Optimize an image by resizing and converting to PNG and WebP formats.

    Args:
        input_path: Path to input image file
        output_path_png: Path for optimized PNG output
        output_path_webp: Path for WebP output

    Returns:
        bool: True if successful, False otherwise
    """
    # Validate input file
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        return False

    if not input_file.is_file():
        print(f"Error: Input path is not a file: {input_file}", file=sys.stderr)
        return False

    # Create output directories if they don't exist
    try:
        Path(output_path_png).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path_webp).parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error: Failed to create output directories: {e}", file=sys.stderr)
        return False

    try:
        with Image.open(input_path) as img:
            print(f"Original dimensions: {img.size}")

            # Resize if width is greater than 1600px
            max_width = 1600
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"Resized to: {img.size}")

            # Save as optimized PNG
            img.save(output_path_png, 'PNG', optimize=True)
            print(f"Successfully saved optimized PNG to {output_path_png}")

            # Save as WebP
            img.save(output_path_webp, 'WEBP', quality=80, lossless=False) # Changed to lossy for better compression
            print(f"Successfully saved optimized WebP to {output_path_webp}")

            old_size = os.path.getsize(input_path)
            new_size_png = os.path.getsize(output_path_png)
            new_size_webp = os.path.getsize(output_path_webp)

            print(f"Original size: {old_size/1024/1024:.2f} MB")
            print(f"Optimized PNG size: {new_size_png/1024/1024:.2f} MB")
            print(f"Optimized WebP size: {new_size_webp/1024/1024:.2f} MB")

            return True

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        return False
    except OSError as e:
        print(f"Error: Failed to process image: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: Unexpected error: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Optimize images by resizing and converting to PNG and WebP formats'
    )
    parser.add_argument(
        'input_file',
        help='Input image file path'
    )
    parser.add_argument(
        '--output-png',
        help='Output PNG file path (default: input_optimized.png)',
        default=None
    )
    parser.add_argument(
        '--output-webp',
        help='Output WebP file path (default: input.webp)',
        default=None
    )

    args = parser.parse_args()

    # Generate default output paths if not provided
    input_path = Path(args.input_file)
    if args.output_png is None:
        output_png = input_path.parent / f"{input_path.stem}_optimized.png"
    else:
        output_png = args.output_png

    if args.output_webp is None:
        output_webp = input_path.parent / f"{input_path.stem}.webp"
    else:
        output_webp = args.output_webp

    success = optimize_image(args.input_file, output_png, output_webp)
    sys.exit(0 if success else 1)

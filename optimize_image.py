from PIL import Image
import os

def optimize_image(input_path, output_path_png, output_path_webp):
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
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_file = r"d:\Development\bryggeriledning\docs\assets\images\Infographic.png"
    output_file_png = r"d:\Development\bryggeriledning\docs\assets\images\Infographic_optimized.png"
    output_file_webp = r"d:\Development\bryggeriledning\docs\assets\images\Infographic.webp"
    optimize_image(input_file, output_file_png, output_file_webp)

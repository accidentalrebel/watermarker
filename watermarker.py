import os
import sys
from PIL import Image
import argparse

def add_watermark(target_dir, watermark_path, output_dir, xOffset=0, yOffset=0, verbose=False):
    # Open the watermark image
    watermark = Image.open(watermark_path)

    # Process each image file in the target directory
    for filename in os.listdir(target_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            if verbose:
                print(f"Processing {filename}")

            image_path = os.path.join(target_dir, filename)
            image = Image.open(image_path)

            # Resize the watermark to fit the width of the target image
            watermark_resized = watermark.resize((image.width, watermark.height * image.width // watermark.width))

            # Calculate the position of the watermark with the given offsets
            x = (image.width - watermark_resized.width) // 2 + xOffset
            y = (image.height - watermark_resized.height) // 2 + yOffset

            # Create a copy of the target image and paste the watermark
            image_with_watermark = image.copy()
            image_with_watermark.paste(watermark_resized, (x, y), watermark_resized)

            # Save the watermarked image to the output directory
            output_path = os.path.join(output_dir, filename)
            image_with_watermark.save(output_path)

            if verbose:
                print(f"Saved watermarked image to {output_path}")

def clear_output_directory(output_dir):
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file: {file_path}. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a watermark to images in a directory.")
    parser.add_argument("target_directory", help="Path to the target directory containing images.")
    parser.add_argument("watermark", help="Path to the watermark image.")
    parser.add_argument("-o", "--output", default="output", help="Path to the output directory.")
    parser.add_argument("-x", "--xOffset", type=int, default=0, help="X-axis offset for the watermark.")
    parser.add_argument("-y", "--yOffset", type=int, default=0, help="Y-axis offset for the watermark.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output.")

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Check if the output directory is empty
    if os.listdir(args.output):
        # Ask the user if they want to overwrite the output directory
        response = input("The output directory is not empty. Do you want to overwrite its contents? [y/N] ").lower()

        if response == 'y':
            clear_output_directory(args.output)
        else:
            print("Aborted.")
            sys.exit(1)

    add_watermark(args.target_directory, args.watermark, args.output, args.xOffset, args.yOffset, args.verbose)

import os
import time
from PIL import Image

def splice_images(input_folder):
    # Create the output folder based on the input folder's name
    output_folder = input_folder + "_spliced"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Calculate the total number of images
    total_images = len(image_files)

    # Define the loading animation
    animation = "|/-\\"
    idx = 0

    # Iterate over each image file
    for i, image_file in enumerate(image_files):
        # Open the image
        image_path = os.path.join(input_folder, image_file)
        image = Image.open(image_path)

        # Calculate the dimensions for each splice
        width, height = image.size
        splice_width = width // 2
        splice_height = height // 2

        # Calculate the coordinates for the splices
        center_x = width // 2
        center_y = height // 2

        # Splice the image into four pieces
        upper_left = image.crop((center_x - splice_width, center_y - splice_height, center_x, center_y))
        upper_right = image.crop((center_x, center_y - splice_height, center_x + splice_width, center_y))
        lower_left = image.crop((center_x - splice_width, center_y, center_x, center_y + splice_height))
        lower_right = image.crop((center_x, center_y, center_x + splice_width, center_y + splice_height))

        # Save the spliced images with original filenames
        spliced_images = [upper_left, upper_right, lower_left, lower_right]
        for j, spliced_image in enumerate(spliced_images):
            filename, extension = os.path.splitext(image_file)
            output_filename = f"{filename}_{j}{extension}"
            output_path = os.path.join(output_folder, output_filename)
            spliced_image.save(output_path)

        # Update the loading animation
        idx = (idx + 1) % len(animation)
        progress = (i + 1) / total_images * 100

        # Display the loading animation and progress
        print(f"\rProcessing image {i + 1}/{total_images} {animation[idx]} {progress:.2f}%", end="")
        time.sleep(0.1)

    print("\nSplicing complete!")

# Example usage
input_folder = "cat-1-4"
splice_images(input_folder)

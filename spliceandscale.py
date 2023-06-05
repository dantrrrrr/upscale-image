import os
import time
from PIL import Image
import replicate
import urllib.request
import ssl

# client = replicate.Client(api_token='r8_YvOE8zNTBXBgNAv4amksd9J2MGXnGQN2xPWAR')
ssl._create_default_https_context = ssl._create_unverified_context

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

# Get the current directory as the input folder
input_folder = input("Enter the path of the input folder: ")

# Splice the images
splice_images(input_folder)

# Get scale from user
scale = int(input("Enter the scale value: "))

# Get face_enhance from user
face_enhance = input("Enter 'True' if face enhancement is required, 'False' otherwise: ").lower() == 'true'

# Create the output folder path
output_folder = os.path.join(input_folder.rstrip('/'), f"output_scaled_{scale}_face_enhance_{str(face_enhance).lower()}")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all image files in the spliced folder
spliced_folder = input_folder + "_spliced"
image_files = [f for f in os.listdir(spliced_folder) if os.path.isfile(os.path.join(spliced_folder, f)) and f.endswith(('.jpg', '.jpeg', '.png'))]

# Iterate over each image file
for i, image_file in enumerate(image_files, start=1):
    # Full path of the input image file
    input_path = os.path.join(spliced_folder, image_file)

    # Process the image using replicate
    output = replicate.run(
        "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
        input={
            "image": open(input_path, "rb"),
            "scale": scale,
            "face_enhance": face_enhance,
        },
    )

    # Save the output image
    image_url = output
    output_path = os.path.join(output_folder, image_file)
    urllib.request.urlretrieve(image_url, output_path)
    print(f"Processed image {i}/{len(image_files)} - Output image saved successfully: {output_path}")

# Print "Finish" after processing all files
print("Progress: Finish")

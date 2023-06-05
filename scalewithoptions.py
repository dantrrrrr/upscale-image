import replicate
import urllib.request
import os
import ssl

# client = replicate.Client(api_token='r8_YvOE8zNTBXBgNAv4amksd9J2MGXnGQN2xPWAR')
ssl._create_default_https_context = ssl._create_unverified_context

# Get input folder path from user
input_folder = input("Enter the path of the input folder: ")

# Get scale from user
scale = int(input("Enter the scale value: "))

# Get face_enhance from user
face_enhance = input("Enter 'True' if face enhancement is required, 'False' otherwise: ").lower() == 'true'

# Create the output folder path
output_folder = os.path.join(input_folder.rstrip('/'), f"output_scaled_{scale}_face_enhance_{str(face_enhance).lower()}")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and f.endswith(('.jpg', '.jpeg', '.png'))]

# Iterate over each image file
for i, image_file in enumerate(image_files, start=1):
    # Full path of the input image file
    input_path = os.path.join(input_folder, image_file)

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

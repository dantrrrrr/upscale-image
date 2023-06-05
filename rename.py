import os

def rename_items(directory):
    counter = 1
    for item in os.listdir(directory):
        if item.endswith(".jpg"):
            item_path = os.path.join(directory, item)
            new_name = f"{counter:04}.png"  # Using a 4-digit zero-padded number for the new name
            new_path = os.path.join(directory, new_name)
            os.rename(item_path, new_path)
            counter += 1

# Specify the directory path where the items are located
directory_path = '/Users/macos/Desktop/cat-1/final-1'

# Call the function to rename items within the directory
rename_items(directory_path)

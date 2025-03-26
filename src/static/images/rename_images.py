import os

def rename_images(directory):
    # Loop through all files in the specified directory
    for filename in os.listdir(directory):
        # Check if the file is an image (you can add more extensions if needed)
        if filename.lower().endswith(('webp', '.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Create a new name by replacing spaces with underscores and converting to lowercase
            new_name = filename.replace(" ", "_").lower()
            # Get the full path for the old and new file names
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_name)
            
            # Rename the file
            os.rename(old_file, new_file)
            print(f'Renamed: "{filename}" to "{new_name}"')

# Specify the directory containing your images
image_directory = './plants'  # Change this to your images directory

# Call the function to rename images
rename_images(image_directory)


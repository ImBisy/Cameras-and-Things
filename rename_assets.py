import os
import re

def rename_inventory_images(directory='img'):
    """
    Renames image files by replacing special characters (:, /, and dots in the name)
    with spaces to match the sanitized server filenames.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' was not found.")
        print("Please make sure the script is in the same folder as your 'img' directory.")
        return

    # Get all files in the directory
    files = os.listdir(directory)
    renamed_count = 0
    skipped_count = 0

    print(f"Scanning directory: {directory}...\n")

    for filename in files:
        # Separate the name from the extension
        name_part, extension = os.path.splitext(filename)
        
        # Only process common image formats
        if extension.lower() not in ['.jpg', '.jpeg', '.png']:
            continue

        # Rule: Replace colons (:), slashes (/), and dots (.) with a space
        # We use regex to find these specific characters
        new_name_part = re.sub(r'[:/.]', ' ', name_part)
        
        # Rule: Clean up double spaces that might have been created
        new_name_part = re.sub(r'\s+', ' ', new_name_part).strip()
        
        # Re-attach the extension
        new_filename = f"{new_name_part}{extension}"

        # If the name actually changed, try to rename the file
        if filename != new_filename:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            
            # Check if the target filename already exists to avoid errors
            if os.path.exists(new_path):
                print(f"Skipped: '{new_filename}' already exists.")
                skipped_count += 1
                continue

            try:
                os.rename(old_path, new_path)
                print(f"SUCCESS: '{filename}' -> '{new_filename}'")
                renamed_count += 1
            except Exception as e:
                print(f"ERROR: Could not rename '{filename}': {e}")
        else:
            # File already matches the format
            pass

    print(f"\n--- Task Complete ---")
    print(f"Files successfully renamed: {renamed_count}")
    print(f"Files skipped (already exist): {skipped_count}")

if __name__ == "__main__":
    # You can run this in your terminal using: python rename_assets.py
    rename_inventory_images()

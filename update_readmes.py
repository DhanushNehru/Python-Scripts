#test
import os

def update_links(readme_path):
    try:
        with open(readme_path, 'r') as file:
            content = file.read()
        
        # Example update: replace 'old-link' with 'new-link'
        updated_content = content.replace('old-link', 'new-link')
        
        with open(readme_path, 'w') as file:
            file.write(updated_content)
        
        print(f"Updated {readme_path}")
    except Exception as e:
        print(f"Failed to update {readme_path}: {e}")

def find_and_update_readmes(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower() == 'readme.md':
                file_path = os.path.join(root, file)
                update_links(file_path)

if __name__ == "__main__":
    root_directory = '.'  # Update this to your repo's root directory if necessary
    find_and_update_readmes(root_directory)



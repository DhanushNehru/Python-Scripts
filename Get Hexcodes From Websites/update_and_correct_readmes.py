import os
import re

# Define a dictionary of common typos and their corrections
typos = {
    'teh': 'the',
    'recieve': 'receive',
    'adn': 'and',
    'occured': 'occurred',
    'seperate': 'separate',
    'definately': 'definitely',
    'goverment': 'government',
    # Add more typos and corrections as needed
}

def correct_typos_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    for typo, correction in typos.items():
        content = re.sub(r'\b' + typo + r'\b', correction, content)

    # Append a comment to indicate the file has been processed
    content += "\n<!-- Updated README links and corrected typos -->"

    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Corrected typos in {file_path}")

def update_links(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Example update: replace 'old-link' with 'new-link'
        updated_content = content.replace('old-link', 'new-link')
        
        with open(file_path, 'w') as file:
            file.write(updated_content)
        
        print(f"Updated {file_path}")
    except Exception as e:
        print(f"Failed to update {file_path}: {e}")

def find_and_process_readmes(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower() == 'readme.md':
                file_path = os.path.join(root, file)
                update_links(file_path)
                correct_typos_in_file(file_path)

if __name__ == "__main__":
    root_directory = '.'  # Set this to your repo's root directory if necessary
    find_and_process_readmes(root_directory)

import pathlib
jpg_files_path = pathlib.Path('Place the folder path here under quotes')
file_paths = []

for file in jpg_files_path.rglob('*'):
    if file.is_file():
        file_paths.append(str(file))

formatted_output = '[\n' + ',\n'.join(f'  "{path}"' for path in file_paths) + '\n]'
print(formatted_output)


file_extensions = []

for file in jpg_files_path.rglob('*'):
    if file.is_file():
        ext = file.suffix.lower()
        if ext and ext not in file_extensions:
            file_extensions.append(ext)


formattedd_output = '[\n' + ',\n'.join(f'  "{ext}"' for ext in file_extensions) + '\n]'
print(formattedd_output)

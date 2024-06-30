import os
import datetime

def get_file_access_time(file_path):
  return os.path.getatime(file_path)

def get_recently_accessed_files(directory_path, time_threshold=None):

  recently_accessed_files = []
  for root, dirs, files in os.walk(directory_path):
    for file in files:
      file_path = os.path.join(root, file)
      file_access_time = get_file_access_time(file_path)

      if time_threshold is None or file_access_time >= time_threshold:
        recently_accessed_files.append(file_path)

  return sorted(recently_accessed_files, key=lambda file_path: get_file_access_time(file_path), reverse=True)

def main():
  
  # Get the directory path to search.
  directory_path = input("Enter the directory path to search: ")

  # Get the list of recently accessed files.
  recently_accessed_files = get_recently_accessed_files(directory_path)

  # Print the list of recently accessed files.
  print("List of recently accessed files:")
  for file_path in recently_accessed_files:
    print(f"{file_path}")

if __name__ == "__main__":
  main()

from faker import Faker
from typing import List
import json

# Initialize Faker with multiple locales
fake = Faker(['it_IT', 'en_US', 'ja_JP'])


def generate_fake_profiles(num_profiles: int) -> List[dict]:
    """
    Generate a list of fake profiles.

    Args:
        num_profiles (int): Number of profiles to generate.

    Returns:
        List[dict]: A list of dictionaries where each represents a profile.
    """
    profiles = []
    for _ in range(num_profiles):
        profile = {
            "Locale": fake.locales,
            "Name": fake.name(),
            "Email": fake.email(),
            "SSN": fake.ssn(),
            "Address": fake.address(),
            "Latitude": fake.latitude(),
            "Longitude": fake.longitude(),
            "URL": fake.url()
        }
        profiles.append(profile)
    return profiles


def display_profiles(profiles: List[dict]):
    """
    Display the generated profiles in a formatted way.

    Args:
        profiles (List[dict]): A list of profiles to print.
    """
    for index, profile in enumerate(profiles, start=1):
        print(f"\n### Faker Profile {index} ###")
        print(f"Locale : {', '.join(profile['Locale'])}")
        print(f"Name : {profile['Name']}")
        print(f"Email : {profile['Email']}")
        print(f"Social Security number (SSN) : {profile['SSN']}")
        print(f"Address : {profile['Address']}")
        print(f"Location : ({profile['Latitude']}, {profile['Longitude']})")
        print(f"URL : {profile['URL']}")
        print("-" * 40)


def save_profiles_to_file(profiles: List[dict], filename: str) -> None:
    """
    Save the list of profiles to a file in JSON format.

    Args:
        profiles (List[dict]): The list of profiles to save.
        filename (str): The name of the output file.
    """
    try:
        with open(filename, "w") as file:
            json.dump(profiles, file, indent=4)
        print(f"\nProfiles successfully saved to {filename}")
    except Exception as e:
        print(f"Error while saving profiles to file: {e}")


def main():
    """
    Main function to handle user interaction and workflow.
    """
    print("\n### Faker Profile Generator ###")
    try:
        num_profiles = int(input("Enter the number of profiles to generate: "))
        if num_profiles < 1:
            raise ValueError("Number of profiles must be greater than 0.")

        # Generate fake profiles
        profiles = generate_fake_profiles(num_profiles)

        # Display profiles
        display_profiles(profiles)

        # Save to file
        save_option = input("Do you want to save the profiles to a file? (y/n): ").strip().lower()
        if save_option == "y":
            filename = input("Enter filename (e.g., profiles.json): ").strip()
            save_profiles_to_file(profiles, filename)

        print("\nProcess completed successfully!")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Run the script
if __name__ == "__main__":
    main()

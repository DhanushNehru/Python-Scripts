import yt_dlp
import cv2
import numpy as np


# -----------------YouTube livestream URLs------------------ #
URLs = [
    # Jellyfish Tank
    "https://www.youtube.com/watch?v=1rvCfsW_qTA",

    # Tropical Reef Aquarium
    "https://www.youtube.com/watch?v=DHUnz4dyb54",

    # Polar Bear Tundra
    "https://www.youtube.com/watch?v=kvJnsuyE0cs",

    # Great Green Macaw Nest
    "https://www.youtube.com/watch?v=OUc-R6Mtg0E",

    # Bison Grasslands National Park
    "https://www.youtube.com/watch?v=g6wxYiESkE4",

    # Puffin Skomer Island
    "https://www.youtube.com/watch?v=1pFTuCQGVZ0",

    # Panda Chengdu Base
    "https://www.youtube.com/watch?v=SUXPnIEpbn4",

    # Grace the Gorilla
    "https://www.youtube.com/watch?v=672cUSe69J0",

    # Bald Eagle Big Bear
    "https://www.youtube.com/watch?v=B4-L2nfGcuE"
]

# yt-dlp set options
options = {
    "quiet": True,
    "no_warnings": True,
    "logger": None
}

def get_single_frame():
    """
    Capture a single frame from a random available YouTube livestream.

    The function randomly iterates through a predefined list of livestream URLs,
    attempts to extract the direct stream URL using yt-dlp, and captures
    one video frame using OpenCV.

    Returns:
        numpy.ndarray:
            A single video frame if capture succeeds.

        None:
            Returned if all livestreams are offline or frame capture fails.
    """

    random_urls = np.random.permutation(URLs)

    for url in random_urls:
        try:

            # Extracts livestream URL and metadata without downloading
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                stream_url = info["url"]

            capture_video = cv2.VideoCapture(stream_url)
            ret, frame = capture_video.read()
            capture_video.release()

            if ret:
                print(f"Frame captured Successfully: {url}")
                return frame

            print(f"Frame capture failed: {url}")

        except Exception as e:
            print(f"{url} livestream currently offline")
            
    print("All livestreams are offline")
    return None


def get_rand_px():
    """
    Extract a random BGR channel value from a random pixel
    within a captured livestream frame.

    A single frame is captured from the first available livestream.
    The function randomly selects:
        - a row position
        - a column position
        - a color channel (B, G, or R)

    Returns:
        int:
            Random pixel channel value between 0 and 255.

        None:
            Returned if frame capture fails.
    """

    frame = get_single_frame()

    if frame is None:
        return None

    # Get a random pixel's BGR value
    h, w, px = frame.shape

    pixel_value = int(frame[np.random.randint(0, h), np.random.randint(0, w),
                            np.random.randint(0, px)])
    print(pixel_value)
    return pixel_value


def sum_all(nums):
    """
    Calculate the sum of all generated random numbers.

    Returns:
        int:
            Sum of all values stored in random_numbers or
            the single stored value if only one number exists.
    """

    return sum(nums)


def avg(nums):
    """
    Calculate the average of all generated random numbers.

     Returns:
        int:
            Rounded average of all values stored in random_numbers or
            the single stored value if only one number exists.
    """

    return round(sum(nums)/len(nums))
    

def concat(nums):
    """
    Concatenate all generated random numbers into a single integer.

    Example:
        [12, 45, 78] -> 124578

    Returns:
        int:
            Concatenated integer of all random numbers or
            the single stored value if only one number exists.
    """

    return int("".join(map(str, nums)))


# -------------------------PROGRAM---------------------------- #
def main():

    random_numbers = []

    size = input("How many random numbers?\n> ")

    while not size.isdigit() or not (1 <= int(size) <= 10):
        print("Error: Please enter an integer between 1 and 10.")

        size = input("How many random numbers? ")

    size = int(size)

    for i in range(size):
        random_numbers.append(get_rand_px())

    while True:

        print("\n>>> COMMANDS <<<")

        print("\n1 : Sum")
        print("2 : Average")
        print("3 : Concatenate")
        print("4 : Print")
        print("5 : Exit")

        COM = input("> ")

        while not COM.isdigit() or not (1 <= int(COM) <= 5):
            print("Error: Please select a number between 1 and 5.")

            print("\n1 : Sum")
            print("2 : Average")
            print("3 : Concatenate")
            print("4 : Print all")
            print("5 : Exit")

            COM = input("> ")

        COM = int(COM)

        if COM == 1:
            print(sum_all(random_numbers))

        elif COM == 2:
            print(avg(random_numbers))

        elif COM == 3:
            print(concat(random_numbers))

        elif COM == 4:
            print(*random_numbers)

        elif COM == 5:
            print("Good Bye")
            break


if __name__ == "__main__":
    main()

## Install Dependencies:

- yt_dlp
- cv2 (OpenCV)
- numpy

Install the required packages:

python -m pip install yt-dlp opencv-python numpy

## How to run:

Run the script in your IDE or from a terminal:

python random_number_generator.py

## How it works:

The script generates random numbers by extracting color-channel values
from random pixels extracted in frames captured from randomly selected
predefined YouTube livestreams.

Process:

```text
Youtube URL 
-> yt_dlp -> extracts the stream URL 
-> cv2 (OpenCV) -> opens the stream and captures a frame
-> numpy -> selects random positions in the frame
-> extracts a random color-channel value
```

### Frame Extraction:

After a frame is captured, its dimensions are extracted:

```python
h = 1080
w = 1920
px = 3
```

Where:

- 'h' = frame height (1080 pixels)
- 'w' = frame width (1920 pixels)
- 'px' = number of channels per pixel

Most YouTube video frames are standard color images, so:

```text
px = 3
```

represents:

```text
Channel 0 -> Blue
Channel 1 -> Green
Channel 2 -> Red
```

The script then randomly selecs:
- A row position
- A column position
- A color channel

Example random selections:

```python
row = 527
column = 1300
channel = 2
```

This returns a frame:

```python
frame[527,1300]
```
which may return:

```python
[45, 182, 230]
```

OpenCV stores colors in BGR order:

```text
Blue = 45
Green = 182
Red = 230
```

Since the randomly selected channel is "2" from:

```python
row = 527
column = 1300
channel = 2
```

The script returns:

```python
230
```

Which is the 3rd element of the channel frame:

```python
[45, 182, 230]
```

## Notes

Because a single color channel is extracted, the generated values currently range between 0-255.
The visual characteristics of the livestream can influence the distribution of values.

Example:

- Snow-heavy videos (such as the Polar Bear Tundra livestream) often contain many bright pixels and may
produce different distributions compared to colorful scenes (such as the Tropical Reef Aquarium).

- Highly colorful streams may produce a wider variety of values.

Future versions may expand the range beyond a single color-channel value.

## Current Available Livestreams

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

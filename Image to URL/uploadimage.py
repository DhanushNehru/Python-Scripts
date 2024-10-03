import base64
import requests
import pyperclip as pc
from PIL import ImageGrab, Image
import os
from dotenv import load_dotenv


device = "mac"
# set device to "windows" if you are on windows, "mac" if you are on macOS
# On windows this uses the keyboard library ( which works only on windows )
# On Mac there is an alternative library called pynput but that requires a lot of permissions
# Which frankly even I am not comfortable since there is a better alternative on mac :
# Open Automator > Create New Document > Choose a Type : Quick Action > Search for "Run Shell Script" > Drag it to the right side > Set Workflow receives input : none > Change shell to python3 > Paste this script in there ( after you have configured everything , like the api_key ... )
# Save that Quick Action. Go to Keyboard Shortcuts > Services > General > Assign your preffered shortcut for the Quick Action you just made.


load_dotenv()
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
api_key_imgbb = os.environ.get("API_KEY_IMGBB")
# api_key_imgbb = "put your imgbb key here ( if not using .env)"


def upload_imgbb():
    img = ImageGrab.grabclipboard()  # grab the current clipboard

    # check if the item is a non image
    if img is None:
        print("Last object was not an image")
        return
    # save the image
    img.save('random.png', 'PNG')

    # open that image in a fileobject
    with open("random.png", "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": api_key_imgbb,
            "image": base64.b64encode(file.read()),
        }

        # send a post request
        res = requests.post(url, payload)  # get the response here
        link = res.json()["data"]["url"]
        print(link)
        # copy the link into our clipboard
        pc.copy(link)
    os.remove("random.png")


if device == "windows":
    import keyboard
    # edit the shortcut (for windows ) here ( check keyboard library documentation/examples )
    keyboard.add_hotkey("ctrl+shift+z", upload_imgbb)
    keyboard.wait('esc')  # pressing esc will exit the background python file
elif device == "mac" or device == "linux":
    upload_imgbb()

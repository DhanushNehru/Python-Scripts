# Image Upload Script

## Overview

This Python script allows users to upload images from their clipboard directly to Imgur by pressing a keyboard shortcut. It utilizes the Imgur API for image uploads and the `python-dotenv` package to manage environment variables securely.

## Features

- **Clipboard Image Capture**: Captures images from the clipboard.
- **Imgur API Integration**: Uploads images to Imgur using a simple API call.
- **Keyboard Shortcut**: Allows users to trigger the upload with a predefined keyboard shortcut (`Ctrl + Alt + S`).
- **Environment Variable Management**: Utilizes a `secret.env` file for managing sensitive data, such as the Imgur Client ID and add it under the name `IMGUR_CLIENT_ID`.


**Note**: You can add an image in your clipboard using `Win + Shift + S`
Also press Esc to end the program 

## Example Screenshot

Here’s how the application looks when running:

![Screenshot of the app](https://i.imgur.com/e35Pvyh.png)
![Screenshot of the app](https://i.imgur.com/ZfyHcsx.png)
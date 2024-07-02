
![pyKeylogger](https://user-images.githubusercontent.com/77505989/162591491-fc2e14ea-3f2e-4d15-a86e-f0e7394a888d.png)

Key loggers are activity-monitoring software programs that give hackers access to your data. The software is installed on your computer and records everything you type. Then it sends this log file to a server, where cybercriminals wait to use all this sensitive information.

### This key logger can not only detect & record your keystrokes but can also:

- Takes screenshot at a particular interval of time

- Records audio

- Record your System’s information & IP Address

- Sends the data to the remote server using [Twilio](https://www.twilio.com/)

- Keep track of your clipboard information

## Technologies on which it is built:
```
1. Python
2. Socket
3. Platform
4. Win32
5. Pynput
6. Scipy
7. Sound-Device
8. Cryptography
9. Twilio
```
## Why pyKeylogger?

- It will broaden the way of thinking of researchers about how we can innovate the key loggers.
- It will help identify the loopholes in the current anti key loggers software.
- Multi software hack: pyKeylogger is packed with many modules to make it more advance than traditional keyloggers.

#### Capable of deleting all the records after sending them to the remote server.
<p align="center">
  <img src="https://user-images.githubusercontent.com/77505989/162591486-e96ab751-bcd1-47b4-b48d-1dc304e06426.png" alt="Delete Records" />
</p>

#### Encrypts the data & generates a new key (Asymmetric Key Encryption) that only the person at the remote server can decrypt.
<p align="center">
  <img src="https://user-images.githubusercontent.com/77505989/162591487-77b5abd9-ab17-4613-a1f2-6618a70b4c84.png" alt="Encryption" />
</p>

#### Using Twilio for transferring the data to a remote server!
<p align="center">
  <img src="https://user-images.githubusercontent.com/77505989/162591488-6682da11-167a-4848-81de-e09d86561830.png" alt="Twilio" />
</p>

## How to use?
After cloning & installing all the dependencies, run
```
>>> python GenerateKey.py
```
It will generate the encryption key. Paste this key into `DecryptFile.py` & `Keylogger.py`. Then run,
```
>>> python Keylogger.py
```
You will see that new files are generating on their own. Watch Demonstration of the project [Here](https://www.youtube.com/watch?v=upWCYSoyOt8).

<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->
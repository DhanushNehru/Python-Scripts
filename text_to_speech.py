import pyttsx3

engine =pyttsx3.init()
voices= engine.getProperty("voices")
for i in voices:
    print(i.id)
    print(i.name)

id ="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
engine.setProperty(i, id)
engine.setProperty("rate",176)
engine.say("hello world")
engine.runAndWait()
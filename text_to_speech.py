import pyttsx3
default_SpeechRate= 176
engine = pyttsx3.init()
voices = engine.getProperty("voices")
for voice in voices:
    print(voice.id)
    print(voice.name)

desired_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
engine.setProperty(voice, desired_voice_id)
engine.setProperty("rate",default_SpeechRate)
engine.say("hello world")
engine.runAndWait()

import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Say something!")
            audio = recognizer.listen(source)

        print(
            "Google Speech Recognition thinks you said: "
            + recognizer.recognize_google(audio)
        )

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    except OSError:
        print(
            "No microphone detected. Please make sure your microphone is connected and configured properly."
        )


recognize_speech()

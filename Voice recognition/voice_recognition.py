import speech_recognition as sr


def recognize_speech(language="en-US"):
    """
    Recognizes speech using Google Speech Recognition.

    Parameters:
    language (str): The language code to be used for recognition.
                    Examples:
                      - "en-US" for English
                      - "es-ES" for Spanish
                      - "pt-BR" for Portuguese (Brazil)
                      - "fr-FR" for French
                      - "ja-JP" for Japanese
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 3

    try:
        with sr.Microphone() as source:
            print("Calibrating ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Please speak now!")

            audio = recognizer.listen(source, timeout=5)

        text = recognizer.recognize_google(audio, language=language)
        print("Google Speech Recognition thinks you said: " + text)

    except sr.WaitTimeoutError:
        print("No speech was detected within the timeout period.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except OSError:
        print(
            "No microphone detected. Please ensure your microphone is connected and configured properly."
        )


if __name__ == "__main__":
    # You can change the language code below as needed:
    recognize_speech(language="es-ES")

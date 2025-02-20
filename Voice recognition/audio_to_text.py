import speech_recognition as sr


def audio_to_text(audio_file, language="en-US"):
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

    try:
        with sr.AudioFile(audio_file) as source:
            print("Processing audio...")
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language=language)
        print("Recognized text:", text)

    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # You can change the language code below as needed:
    # Supported formats: WAV, AIFF, AIFF-C, FLAC (MP3 and others require conversion)
    # Provide the full path to the audio file
    audio_to_text("C:/Users/YourUser/Music/audio.wav", language="en-US")

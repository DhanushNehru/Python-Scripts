morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
    '8': '---..', '9': '----.', '0': '-----', ' ': '/'
}

def encode_to_morse(text):
    try:
        return ' '.join(morse_code_dict[char] for char in text.upper() if char in morse_code_dict)
    except KeyError:
        print("Error: Input contains unsupported characters.")

def decode_from_morse(morse_code):
    try:
        morse_words = morse_code.split(' / ')
        decoded_message = ''
        for word in morse_words:
            decoded_message += ''.join(
                [char for morse_char in word.split() for char, code in morse_code_dict.items() if code == morse_char]
            ) + ' '
        return decoded_message.strip()
    except Exception as e:
        print("Error during decoding:", e)

def menu():
    while True:
        print("\nMorse Code Encoder/Decoder")
        print("1. Encode Text to Morse Code")
        print("2. Decode Morse Code to Text")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            text = input("Enter text to encode: ")
            encoded = encode_to_morse(text)
            print("Encoded Morse Code:", encoded)
        
        elif choice == '2':
            morse_code = input("Enter Morse code to decode (use '/' for spaces): ")
            decoded = decode_from_morse(morse_code)
            print("Decoded Text:", decoded)
        
        elif choice == '3':
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    menu()

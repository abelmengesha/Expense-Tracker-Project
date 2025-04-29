import winsound
import time

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
    '0': '-----', ' ': '/'
}

DOT_DURATION = 200  # Duration of dot sound in milliseconds
DASH_DURATION = 600  # Duration of dash sound in milliseconds
FREQ = 800  # Frequency of sound

def text_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

def play_morse_code(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            winsound.Beep(FREQ, DOT_DURATION)
        elif symbol == '-':
            winsound.Beep(FREQ, DASH_DURATION)
        elif symbol == ' ':
            time.sleep(0.2)  # Short pause between characters
        elif symbol == '/':
            time.sleep(0.5)  # Pause between words

def main():
    text = input("Enter text to convert to Morse Code: ")
    morse_code = text_to_morse(text)
    print(f"Morse Code: {morse_code}")
    play_morse_code(morse_code)

if __name__ == "__main__":
    main()

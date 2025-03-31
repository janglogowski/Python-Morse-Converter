import pandas as pd

class MorseLogic:
    def __init__(self):
        self.alphabet = self.create_alphabet_dict()
        self.reverse_alphabet = {code: letter for letter, code in self.alphabet.items()}

    def create_alphabet_dict(self):
        alphabet = pd.read_csv('morse_phonetic_alphabet.csv')
        df_alphabet = pd.DataFrame(alphabet)
        return {row.letter:row.code for _, row in df_alphabet.iterrows()}

    def encode_text(self, input_text):
        encoded = [self.alphabet.get(letter.lower(), letter) for letter in input_text]
        return ' '.join(encoded)

    def decode_morse(self, morse_code):
        morse_code = morse_code.replace('.', '•').replace('-', '−')
        words = morse_code.split(' / ')
        decoded_words = []
        
        for word in words:
            letters = word.split()
            decoded_word = ''.join(self.reverse_alphabet.get(letter, '(?)') for letter in letters)
            decoded_words.append(decoded_word)
        return ' '.join(decoded_words)
import pandas as pd

class MorseLogic:
    def __init__(self):
        self.alphabet = self.create_alphabet_dict()

    def create_alphabet_dict(self):
        alphabet = pd.read_csv('morse_phonetic_alphabet.csv')
        df_alphabet = pd.DataFrame(alphabet)
        alphabet_dict = {row.letter:row.code for _, row in df_alphabet.iterrows()}
        return alphabet_dict

    def generate_phonetic(self, input_text):
        encoded = []
        for letter in input_text.lower():
            if letter in self.alphabet:
                encoded.append(self.alphabet[letter])
            else:
                encoded.append(letter)
        return encoded
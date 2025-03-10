import pandas as pd

class MorseLogic():
    def __init__(self):
        super().__init__()
        self.alphabet_dict = self.create_alphabet_dict()

#--------READING DATA--------# 
    def create_alphabet_dict(self):
        alphabet = pd.read_csv('morse_phonetic_alphabet.csv')
        df_alphabet = pd.DataFrame(alphabet)
        alphabet_dict = {row.letter:row.code for _, row in df_alphabet.iterrows()}
        return alphabet_dict

#--------ENCODING DATA--------# 
    def generate_phonetic(self):
        try:
            user_word = input("enter a word: ").lower()
            word_encoded = [self.alphabet_dict[letter] for letter in user_word]
        except KeyError:
            print("Sorry, only letters in the alphabet please.")
            self.generate_phonetic()
        else:
            print(word_encoded)
            return word_encoded

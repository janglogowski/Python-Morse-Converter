import pandas as pd

#--------READING DATA--------# 
alphabet = pd.read_csv('morse_phonetic_alphabet.csv')
df_alphabet = pd.DataFrame(alphabet)

alphabet_dict = {row.letter:row.code for (index, row) in df_alphabet.iterrows()}

#--------ENCODING DATA--------# 
def generate_phonetic():
    try:
        user_word = input("enter a word: ").lower()
        word_encoded = [alphabet_dict[letter] for letter in user_word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(word_encoded)
        return word_encoded
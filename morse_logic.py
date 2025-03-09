import pandas as pd

#--------READING DATA--------# 
alphabet = pd.read_csv('morse_phonetic_alphabet.csv')
df_alphabet = pd.DataFrame(alphabet)
print(df_alphabet)

alphabet_dict = {row.letter:row.code for (index, row) in df_alphabet.iterrows()}
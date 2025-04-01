#---------------------------IMPORTS----------------------------# 
import random
from morse_logic import MorseLogic
from audio import play_sound
from tkinter import Button, END

#---------------------------PLAYMODE---------------------------# 
class PlayMode:
    def __init__(self, parent):
        self.morse_logic = MorseLogic()
        self.alphabet = self.morse_logic.alphabet
        self.first_choice = True
        self.random_letter = ''
        self.score = 0
        self.highscore = self.load_highscore()
        self.parent = parent 

    def choose_type(self):
        self.parent.display.config(text='')
        self.parent.user_answer.delete('1.0', END)

        type_dict = {1: self.letter_to_code,
                     2: self.code_to_letter,
                     3: self.audio_to_letter}

        if self.first_choice:
            self.type = random.randint(1, 2)
            self.first_choice = False
        else:
            self.type = random.randint(1, 3)
        type_dict[self.type]()

    def letter_to_code(self):
        self.parent.display_label.config(text='Guess the code: ')

        while True:
            self.random_letter = random.choice(list(self.alphabet))
            if self.random_letter != ' ':
                break
        self.parent.display.config(text=self.random_letter)

    def code_to_letter(self):
        self.parent.display_label.config(text='Guess the letter: ')

        while True:
            self.random_letter = random.choice(list(self.alphabet))
            if self.random_letter != ' ':
                break
        random_code = self.morse_logic.encode_text(self.random_letter)
        self.parent.display.config(text=random_code)

    def audio_to_letter(self):
        self.parent.display_label.config(text='Guess the letter: ')

        while True:
            self.random_letter = random.choice(list(self.alphabet))
            if self.random_letter != ' ':
                break

        self.play_btn = Button(self.parent,
                               text='▶',
                               bg='#dcdcdc',
                               font=('Arial', 22, 'bold'),
                               width=11,
                               command=self.play_random_sound)
        self.play_btn.grid(column=1, row=2, columnspan=3)

    def play_random_sound(self):
        random_code = self.morse_logic.encode_text(self.random_letter)
        random_code = " ".join(random_code)
        play_sound(random_code)

    def check_answer(self):
        user_answer = self.parent.user_answer.get('1.0', END).strip().lower()

        if self.type == 1:
            correct_answer = self.morse_logic.encode_text(self.random_letter)[0]
            correct_answer = correct_answer.replace('•', '.').replace('−', '-')
        else:
            correct_answer = self.random_letter.lower()

        if user_answer == correct_answer:
            self.score += 1
            self.parent.score_label.config(text=f'Score: {self.score}')
            if self.score > self.highscore:
                self.highscore = self.score
                self.parent.highscore_label.config(text=f'High Score: {self.highscore}')
                self.save_highscore()

            if hasattr(self, 'play_btn'):
                self.play_btn.grid_forget()
            self.choose_type()

    def load_highscore(self):
        try:
            with open('highest_score.txt', 'r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        with open('highest_score.txt', 'w') as file:
            file.write(str(self.highscore))

    def reset(self):
        self.score = 0
        self.parent.score_label.config(text=f'Score: {self.score}')
        self.first_choice = True
        self.parent.display.config(text='')
        self.parent.user_answer.delete('1.0', END)

        if hasattr(self, 'play_btn'):
            self.play_btn.grid_forget()
        self.choose_type()
#---------------------------IMPORTS----------------------------# 
from tkinter import *
from PIL import Image, ImageTk
from morse_logic import MorseLogic
from config import *
from audio import play_sound, download_sound
import random
import time

#--------------------------MORSE APP---------------------------# 
class MorseApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Morse Code Converter App")
        self.config(bg=BACKGROUND)
        self.geometry(WINDOW_SIZE)

        self.frames = {}
        for frame_class in (MainFrame, EncodeFrame, DecodeFrame, LearnFrame):
            frame = frame_class(self)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(MainFrame)

    def show_frame(self,frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

#------------------------MAIN GUI FRAME------------------------# 
class MainFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self.create_main_widgets()
        self.create_main_buttons()

    def create_main_widgets(self):
        app_name = Label(self,
                         text='Morse Code Converter',
                         font=(FONT_NAME,51,'italic','bold'),
                         bg=BACKGROUND,
                         fg='white',
                         justify='left')
        app_name.grid(column=0,row=0,padx=30,pady=(20,0),columnspan=3,sticky='nsew') 

        img = Image.open(PHOTO_MAIN)
        img = img.resize((750,300))
        self.photo = ImageTk.PhotoImage(img)
        image_label = Label(self, image=self.photo,bg=BACKGROUND)
        image_label.grid(column=1,row=1,pady=10)

        label = Label(self,
                      text='Welcome to Morse Code Converter! Choose one:',
                      font=(FONT_NAME,20),
                      bg=BACKGROUND,
                      fg='white',
                      justify='left',
                      width=40)
        label.grid(column=0,row=2,padx=30,pady=20,columnspan=3)

    def create_main_buttons(self):
        buttons = [('Encode', EncodeFrame),
                   ('Decode', DecodeFrame),
                   ('Learn',LearnFrame)]
        
        for i, (text, frame) in enumerate(buttons):
            button = Button(self,
                            text=text,
                            font=(FONT_NAME,15),
                            width=40,
                            bg=BUTTON_BACKGROUND,
                            fg='white',
                            command=lambda f=frame: self.master.show_frame(f))
            button.grid(column=1, row=3+i, pady=3)

#-----------------------ENCODE GUI FRAME-----------------------# 
class EncodeFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self.input_text = 'Type in text to encode.'
        self.morse_logic = MorseLogic()

        for i in range(0,15):  
            self.grid_columnconfigure(i, weight=1,minsize=30)  
            if i < 10:  
                self.grid_rowconfigure(i, weight=1,minsize=15)

        self.create_encode_widgets()
        self.create_keyboard()
        self.monitor_user_input()
        self.user_input.bind("<KeyPress>", self.on_key_press_event)

    def create_keyboard(self):
        alphabet_dict = self.morse_logic.alphabet

        self.btn_dict = {}
        self.letters = list(alphabet_dict.keys())
        self.codes = list(alphabet_dict.values())

        column_n,row_n = 1,1

        for i in range(len(self.letters)):
            alphabet_button = Button(self,
                                     text=f'{self.letters[i].upper()}\n{self.codes[i]}',
                                     font=(FONT_NAME,13),
                                     width=5,
                                     bg=BUTTON_BACKGROUND,
                                     fg='white',
                                     activebackground='#bcbcbc',
                                     activeforeground='white')
            alphabet_button.grid(column=column_n, row=row_n, sticky='nsew',pady=1,padx=1)
            column_n += 1

            if column_n == 14:
                column_n = 1
                row_n += 1
            
            self.btn_dict[self.letters[i].lower()] = alphabet_button

    def create_encode_widgets(self):
        play_button = Button(self,
                             text="Play Audio",
                             font=(FONT_NAME,15),
                             width=32,
                             bg=BUTTON_BACKGROUND,
                             fg='white',
                             command=self.play_audio)
        play_button.grid(column=1,row=9,columnspan=7,pady=(0,7),padx=(0,36))

        download_button = Button(self,
                                 text="Download Audio",
                                 font=(FONT_NAME,15),
                                 width=32,
                                 bg=BUTTON_BACKGROUND,
                                 fg='white',
                                 command=self.download_audio)
        download_button.grid(column=7,row=9,columnspan=7,pady=(0,7),padx=(41,0))       

        back_button = Button(self,
                             text="Back",
                             font=(FONT_NAME,15),
                             width=67,
                             bg=BUTTON_BACKGROUND,
                             fg='white',
                             command=lambda: self.master.show_frame(MainFrame))
        back_button.grid(column=1,row=10,columnspan=13)

        self.user_input = Text(self,
                               font=(FONT_NAME,12),
                               wrap='word',
                               width=82,
                               height=9)
        self.user_input.insert(END, self.input_text)
        self.user_input.grid(column=1,row=5,columnspan=13)

        self.text_output = Text(self,
                                font=(FONT_NAME,12),
                                wrap='word',
                                width=82,
                                height=9)
        self.text_output.grid(column=1,row=7,columnspan=13)

    def monitor_user_input(self):
        text_to_encode = self.user_input.get('1.0',END).strip()

        if text_to_encode != self.input_text:
            self.input_text = text_to_encode
                
            encoded_text = self.morse_logic.generate_code(text_to_encode)
            self.encoded_output(encoded_text)

        self.after(100,self.monitor_user_input)

    def on_key_press_event(self, event):
        pressed_key = event.char.lower() 

        if pressed_key in self.btn_dict: 
            self.btn_dict[pressed_key].config(bg='#bcbcbc')
            self.after(100, lambda: self.btn_dict[pressed_key].config(bg=BUTTON_BACKGROUND))

#-----------------------SOUND SETTINGS-------------------------# 
    def play_audio(self):
        text_to_audio = self.text_output.get('1.0', END).strip()
        if text_to_audio:
            play_sound(text_to_audio)
            
    def encoded_output(self,u_input):
        self.text_output.delete(1.0, END)
        self.text_output.insert(END, u_input)

    def download_audio(self):
        text_input = self.user_input.get('1.0', END).strip()
        text_to_audio = self.text_output.get('1.0', END).strip()

        if text_input:
            download_sound(text_to_audio, text_input)

#--------LEARN MODE GUI FRAME--------# 
class LearnFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)

        self.morse_logic = MorseLogic()
        self.alphabet = self.morse_logic.alphabet
        self.first_choice = True
        self.random_letter = ''
        self.score = 0
        self.highscore = self.load_highscore()

        for i in range(0,5):  
            self.grid_columnconfigure(i, weight=1)  

        self.create_scoreboard()
        self.create_widgets()
        self.choose_type()

    def create_scoreboard(self):
        self.score_label = Label(self, 
                      text=f'Score: {self.score}',
                      font=(FONT_NAME,20,'bold'),
                      bg=BACKGROUND,
                      fg='white')
        self.score_label.grid(column=1,row=0,pady=(20,0),sticky='w',padx=20)

        self.highscore_label = Label(self, 
                      text=f'High Score: {self.highscore}',
                      font=(FONT_NAME,20,'bold'),
                      bg=BACKGROUND,
                      fg='white')
        self.highscore_label.grid(column=3,row=0,pady=(20,0),sticky='e',padx=20)

    def create_widgets(self):
        img = Image.open(PHOTO_LEARN)
        img = img.resize((750,300))
        self.photo = ImageTk.PhotoImage(img)
        image_label = Label(self, image=self.photo,bg=BACKGROUND)
        image_label.grid(column=1,row=1,pady=(10,15),padx=10,columnspan=3)

        self.display_label = Label(self,
                                   text='',
                                   font=(FONT_NAME,20,'italic'),
                                   bg=BACKGROUND,
                                   fg='white')
        self.display_label.grid(column=1,row=2,pady=(0,10),sticky='nsew')

        self.display = Label(self,
                             text='',
                             bg='#dcdcdc',
                             font=(FONT_NAME,25,'bold'),
                             width=9)
        self.display.grid(column=1,row=2,columnspan=3)

        self.user_answer = Text(self,
                          font=(FONT_NAME,25),
                          width=10,
                          height=1)
        self.user_answer.grid(column=1,row=3,columnspan=3,pady=(25,5))

        guess_button = Button(self,
                              text="Guess",
                              font=(FONT_NAME,15),
                              width=16,
                              bg=BUTTON_BACKGROUND,
                              fg='white',
                              command=self.check_answer)
        guess_button.grid(column=1,row=4,columnspan=3,pady=(5,0))

        back_button = Button(self,
                              text="Back",
                              font=(FONT_NAME,15),
                              width=40,
                              bg=BUTTON_BACKGROUND,
                              fg='white',
                              command=lambda: self.reset() or self.master.show_frame(MainFrame))
        back_button.grid(column=1,row=5,columnspan=3,pady=(50,0))

#------------------------PLAY MODE SETTINGS------------------------# 
    def choose_type(self):
        self.display.config(text='')
        self.user_answer.delete('1.0', END)

        type_dict = {1:self.letter_to_code,
                     2:self.code_to_letter,
                     3:self.audio_to_letter}
        
        if self.first_choice:
            self.type = random.randint(1,2)
            self.first_choice = False
        else:
            self.type = random.randint(1,3)
        type_dict[self.type]()

    def letter_to_code(self):
        self.display_label.config(text='Guess the code: ')

        while True:
            self.random_letter = random.choice(list(self.alphabet))
            if self.random_letter != ' ':
                break
        self.display.config(text=self.random_letter)

    def code_to_letter(self):
        self.display_label.config(text='Guess the letter: ')

        while True:
            self.random_letter = random.choice(list(self.alphabet))
            if self.random_letter != ' ':
                break
        random_code = self.morse_logic.generate_code(self.random_letter)
        self.display.config(text=random_code)

    def audio_to_letter(self):
        self.display_label.config(text='Guess the letter: ')

        while True:
            self.random_letter = random.choice(list(self.alphabet))
            if self.random_letter != ' ':
                break

        self.play_btn = Button(self,
                            text='▶',
                            bg='#dcdcdc',
                            font=(FONT_NAME, 22, 'bold'),
                            width=11,
                            command=self.play_random_sound)
        self.play_btn.grid(column=1, row=2, columnspan=3)

    def play_random_sound(self):
        random_code = self.morse_logic.generate_code(self.random_letter)
        random_code = " ".join(random_code)
        play_sound(random_code)

    def check_answer(self):
        user_answer = self.user_answer.get('1.0',END).strip().lower()

        if self.type == 1:
            correct_answer = self.morse_logic.generate_code(self.random_letter)[0]
            correct_answer = correct_answer.replace('•','.').replace('−','-')
        else:
            correct_answer = self.random_letter.lower()

        if user_answer == correct_answer:
            self.score += 1
            self.score_label.config(text=f'Score: {self.score}')
            if self.score > self.highscore:
                self.highscore = self.score
                self.highscore_label.config(text=f'High Score: {self.highscore}')
                self.save_highscore()

            if hasattr(self, 'play_btn'):
                self.play_btn.grid_forget()
            self.choose_type()

    def load_highscore(self):
        try:
            with open('highest_score.txt','r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_highscore(self):
        with open('highest_score.txt', 'w') as file:
            file.write((str(self.highscore)))

    def reset(self):
        self.score = 0
        self.score_label.config(text=f'Score: {self.score}')
        self.first_choice = True
        self.display.config(text='')
        self.user_answer.delete('1.0', END)
        self.choose_type()

#-----------------------DECODE GUI FRAME-----------------------# 
class DecodeFrame(Frame):
    pass

if __name__ == "__main__":
    morse_app = MorseApp()
    morse_app.mainloop()
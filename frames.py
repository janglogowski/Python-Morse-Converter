#---------------------------IMPORTS----------------------------# 
from tkinter import *
from PIL import Image, ImageTk
from morse_logic import MorseLogic
from config import *
from audio import play_sound, download_sound
from playmode import PlayMode

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
        buttons = [('Encode/Decode Mode', EncodeFrame),
                   ('Learn Mode',LearnFrame)]
        
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
        self.input_text = ''
        self.output_text = ''
        self.updating_input = False
        self.updating_output = False

        self.morse_logic = MorseLogic()

        for i in range(0,15):  
            self.grid_columnconfigure(i, weight=1,minsize=30)  
            if i < 10:  
                self.grid_rowconfigure(i, weight=1,minsize=15)

        self.create_encode_widgets()
        self.create_keyboard()
        self.monitor_user_input()
        self.monitor_user_output()
        self.user_input.bind("<KeyPress>", self.on_key_press_event)

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
                                     activeforeground='white',
                                     command=lambda letter=self.letters[i]: self.btn_insert(letter))
            alphabet_button.grid(column=column_n, row=row_n, sticky='nsew',pady=1,padx=1)
            column_n += 1

            if column_n == 14:
                column_n = 1
                row_n += 1
            
            self.btn_dict[self.letters[i].lower()] = alphabet_button

    def monitor_user_input(self):
        if not self.updating_output and self.user_input.focus_get() == self.user_input:  
            text_to_encode = self.user_input.get('1.0', END).strip()

            if text_to_encode != self.input_text:
                self.input_text = text_to_encode
                encoded_text = self.morse_logic.encode_text(text_to_encode)

                self.updating_input = True
                self.text_output.delete(1.0, END)
                self.text_output.insert(END, encoded_text)
                self.updating_input = False

        self.after(100, self.monitor_user_input)

    def monitor_user_output(self):
        if not self.updating_input and self.text_output.focus_get() == self.text_output:  
            text_to_decode = self.text_output.get('1.0', END).strip()

            if text_to_decode != self.output_text:
                self.output_text = text_to_decode
                decoded_text = self.morse_logic.decode_morse(text_to_decode)

                self.updating_output = True
                self.user_input.delete(1.0, END)
                self.user_input.insert(END, decoded_text)
                self.updating_output = False

        self.after(100, self.monitor_user_output)

    def on_key_press_event(self, event):
        pressed_key = event.char.lower() 
        if pressed_key in self.btn_dict: 
            self.btn_dict[pressed_key].config(bg='#bcbcbc')
            self.after(100, lambda: self.btn_dict[pressed_key].config(bg=BUTTON_BACKGROUND))

    def btn_insert(self,letter):
        self.user_input.insert(END, letter)

    def encoded_output(self,u_input):
        self.text_output.delete(1.0, END)
        self.text_output.insert(END, u_input)

    def decoded_output(self, decoded_text):
        self.user_input.delete(1.0, END)
        self.user_input.insert(END, decoded_text)
        
#-----------------------SOUND SETTINGS-------------------------# 
    def play_audio(self):
        text_to_audio = self.text_output.get('1.0', END).strip()
        if text_to_audio:
            play_sound(text_to_audio)

    def download_audio(self):
        text_input = self.user_input.get('1.0', END).strip()
        text_to_audio = self.text_output.get('1.0', END).strip()

        if text_input:
            download_sound(text_to_audio, text_input)

#--------LEARN MODE GUI FRAME--------# 
class LearnFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self.play_mode = PlayMode(self)
        self.score = self.play_mode.score
        self.highscore = self.play_mode.highscore

        for i in range(0,5):  
            self.grid_columnconfigure(i, weight=1)  

        self.create_scoreboard()
        self.create_learn_widgets()
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

    def create_learn_widgets(self):
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
                              command=self.play_mode.check_answer)
        guess_button.grid(column=1,row=4,columnspan=3,pady=(5,0))

        back_button = Button(self,
                              text="Back",
                              font=(FONT_NAME,15),
                              width=40,
                              bg=BUTTON_BACKGROUND,
                              fg='white',
                              command=lambda: self.play_mode.reset() or self.master.show_frame(MainFrame))
        back_button.grid(column=1,row=5,columnspan=3,pady=(50,0))

    def choose_type(self):
        self.play_mode.choose_type()

    def check_answer(self):
        self.play_mode.check_answer()

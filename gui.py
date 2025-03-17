#------------------------IMPORTS------------------------# 
from tkinter import *
from PIL import Image, ImageTk
from morse_logic import *
from config import *
from audio import play_sound
from morse_logic import *

#------------------MORSE APP-------------------# 
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

#--------MAIN GUI FRAME--------# 
class MainFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self.create_widgets()

#--------CREATING WIDGETS--------# 
    def create_widgets(self):
        app_name = Label(self,
                         text='Morse Code Converter',
                         font=(FONT_NAME,51,'italic','bold'),
                         bg=BACKGROUND,
                         fg='white',
                         justify='left')
        app_name.grid(column=0,row=0,padx=30,pady=(20,0),columnspan=3,sticky='nsew') 

        img = Image.open(PHOTO)
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

        encode_button = Button(self,
                               text="Encode",
                               font=(FONT_NAME,15),
                               width=40,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=lambda: self.master.show_frame(EncodeFrame))
        encode_button.grid(column=1,row=3)

        decode_button = Button(self,
                               text="Decode",
                               font=(FONT_NAME,15),
                               width=40,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command= lambda: self.master.show_frame(DecodeFrame))
        decode_button.grid(column=1,row=4,pady=7)

        learn_button = Button(self,
                              text="Learn",
                              font=(FONT_NAME,15),
                              width=40,
                              bg=BUTTON_BACKGROUND,
                              fg='white',
                              command=lambda: self.master.show_frame(LearnFrame))
        learn_button.grid(column=1,row=5)

#--------ENCODE GUI FRAME--------# 
class EncodeFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self.input_text = 'Type in text to encode.'

        self.morse_logic = MorseLogic()

        for i in range(0,15):  
            self.grid_columnconfigure(i, weight=1,minsize=30)  
            if i < 10:  
                self.grid_rowconfigure(i, weight=1,minsize=15)

        self.create_keyboard()
        self.create_widgets()

        self.monitor_user_input()
        self.user_input.bind("<KeyPress>", self.on_key_press)

#--------CREATING ENCODE FRAME KEYBOARD--------#
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
                                     fg='white')
            alphabet_button.grid(column=column_n, row=row_n, sticky='nsew',pady=1,padx=1)
            column_n += 1

            if column_n == 14:
                column_n = 1
                row_n += 1
            
            self.btn_dict[self.letters[i].lower()] = alphabet_button

#--------CREATING WIDGETS--------# 
    def create_widgets(self):
        play_button = Button(self,
                                text="Play Audio",
                                font=(FONT_NAME,15),
                                width=67,
                                bg=BUTTON_BACKGROUND,
                                fg='white',
                                command=self.play_sound)
        play_button.grid(column=1,row=9,columnspan=13,pady=(0,7))

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

#--------MONITORING INPUT--------#
    def monitor_user_input(self):
        text_to_encode = self.user_input.get('1.0',END).strip()

        if text_to_encode != self.input_text:
            self.input_text = text_to_encode
                
            encoded_text = self.morse_logic.generate_phonetic(text_to_encode)
            self.encoded_output(encoded_text)

        self.after(100,self.monitor_user_input)

#--------KEYBOARD INPUT HANDLING--------# 
    def on_key_press(self, event):
        pressed_key = event.char.lower() 

        if pressed_key in self.btn_dict: 
            self.btn_dict[pressed_key].config(bg='#bcbcbc')
            self.after(100, lambda: self.btn_dict[pressed_key].config(bg=BUTTON_BACKGROUND))

#--------PLAYING SOUND--------#
    def play_sound(self):
        codes = self.text_output.get('1.0', END).strip()
        play_sound(codes)
            
#--------ENCODED OUTPUT--------# 
    def encoded_output(self,u_input):
        self.text_output.delete(1.0, END)
        self.text_output.insert(END, u_input)

#--------DECODE GUI FRAME--------# 
class DecodeFrame(Frame):
    pass

#--------LEARN MODE GUI FRAME--------# 
class LearnFrame(Frame):
    pass
from tkinter import *
from PIL import Image, ImageTk
from morse_logic import *

#--------CONSTANTS--------# 
BACKGROUND = '#242424'
BUTTON_BACKGROUND = '#828282'
FONT_NAME = 'Chicago'
WINDOW_SIZE = "800x670"

#--------CREATING GUI CLASS--------# 
class Gui(Tk):
    def __init__(self):
        super().__init__()
        self.title("Morse Code Converter App")
        self.config(bg=BACKGROUND)
        self.geometry(WINDOW_SIZE)

        self.frames = {
            'main': Frame(self,bg=BACKGROUND),
            'encode': Frame(self,bg=BACKGROUND),
            'decode': Frame(self,bg=BACKGROUND),
            'learn': Frame(self,bg=BACKGROUND)
        }

        self.current_frame = None
        self.morse_logic = MorseLogic()

        self.main_frame()

#--------CLEANING FRAMES--------# 
    def frame_clear(self):
        for frame in self.frames.values():
            frame.grid_forget()
        self.current_frame = None

#--------SWITCHING BETWEEN FRAMES--------# 
    def show_frame(self,frame_name):
        self.frame_clear()
        self.frames[frame_name].grid(column=0, row=0, sticky="nsew")
        self.current_frame = frame_name

#--------MAIN GUI FRAME--------# 
    def main_frame(self):
        self.show_frame('main')

        for i in range(3):
            self.frames['main'].grid_columnconfigure(i, weight=1)  

        app_name = Label(self.frames['main'],
                         text='Morse Code Converter',
                         font=(FONT_NAME,51,'italic','bold'),
                         bg=BACKGROUND,
                         fg='white',
                         justify='left')
        app_name.grid(column=0,row=0,padx=30,pady=(20,0),columnspan=3,sticky='nsew') 

        img = Image.open('machine.jpg')
        img = img.resize((750,300))
        self.photo = ImageTk.PhotoImage(img)
        image_label = Label(self.frames['main'], image=self.photo,bg=BACKGROUND)
        image_label.grid(column=1,row=1,pady=10)

        label = Label(self.frames['main'],text='Welcome to Morse Code Converter! Choose one:',
                           font=(FONT_NAME,20),
                           bg=BACKGROUND,
                           fg='white',
                           justify='left',
                           width=40)
        label.grid(column=0,row=2,padx=30,pady=20,columnspan=3)

        encode_button = Button(self.frames['main'],
                               text="Encode",
                               font=(FONT_NAME,15),
                               width=40,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.encode_frame)
        encode_button.grid(column=1,row=3)

        decode_button = Button(self.frames['main'],
                               text="Decode",
                               font=(FONT_NAME,15),
                               width=40,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.decode_frame)
        decode_button.grid(column=1,row=4,pady=7)

        learn_button = Button(self.frames['main'],
                              text="Learn",
                              font=(FONT_NAME,15),
                              width=40,
                              bg=BUTTON_BACKGROUND,
                              fg='white',
                              command=self.learn_frame)
        learn_button.grid(column=1,row=5)

#--------ENCODE GUI FRAME--------# 
    def encode_frame(self):
        self.show_frame('encode')
        self.input_text = "Enter a message to encode."

        for i in range(0,15):  
            self.frames['encode'].grid_columnconfigure(i, weight=1,minsize=30)  
            if i < 10:  
                self.frames['encode'].grid_rowconfigure(i, weight=1,minsize=15)

        self.create_keyboard()

        play_button = Button(self.frames['encode'],
                               text="Play Audio",
                               font=(FONT_NAME,15),
                               width=32,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.main_frame)
        play_button.grid(column=1,row=9,columnspan=7,pady=(0,7),padx=(0,36))

        download_button = Button(self.frames['encode'],
                               text="Download Audio",
                               font=(FONT_NAME,15),
                               width=32,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.main_frame)
        download_button.grid(column=7,row=9,columnspan=7,pady=(0,7),padx=(41,0))

        back_button = Button(self.frames['encode'],
                               text="Back",
                               font=(FONT_NAME,15),
                               width=67,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.main_frame)
        back_button.grid(column=1,row=10,columnspan=13)

        self.user_input = Text(self.frames['encode'],
                          font=(FONT_NAME,12),
                          wrap='word',
                          width=82,
                          height=9)
        self.user_input.insert(END, self.input_text)
        self.user_input.grid(column=1,row=5,columnspan=13)

        self.text_output = Text(self.frames['encode'],
                          font=(FONT_NAME,12),
                          wrap='word',
                          width=82,
                          height=9)
        self.text_output.grid(column=1,row=7,columnspan=13)

        self.monitor_user_input()
        self.user_input.bind("<KeyPress>", self.on_key_press)

#--------MONITORING INPUT--------#
    def monitor_user_input(self):
        if self.current_frame == 'encode' and hasattr(self,'user_input'):
            text_to_encode = self.user_input.get('1.0',END).strip()

            if text_to_encode != self.input_text:
                self.input_text = text_to_encode
                
                encoded_text = self.morse_logic.generate_phonetic(text_to_encode)
                self.encoded_output(encoded_text)

        self.after(100,self.monitor_user_input)

#--------CREATING ENCODE KEYBOARD--------#
    def create_keyboard(self):
        self.btn_dict = {}
        alphabet_dict = self.morse_logic.alphabet
        self.letters = list(alphabet_dict.keys())
        self.codes = list(alphabet_dict.values())

        column_n,row_n = 1,1

        for i in range(len(self.letters)):
            alphabet_button = Button(self.frames['encode'],
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

#--------KEYBOARD INPUT HANDLING--------# 
    def on_key_press(self, event):
        pressed_key = event.char.lower() 

        if pressed_key in self.btn_dict: 
            self.btn_dict[pressed_key].config(bg='#bcbcbc')
            self.after(100, lambda: self.btn_dict[pressed_key].config(bg=BUTTON_BACKGROUND))
            
#--------ENCODED OUTPUT--------# 
    def encoded_output(self,u_input):
        self.text_output.delete(1.0, END)
        self.text_output.insert(END, u_input)

#--------DECODE GUI FRAME--------# 
    def decode_frame(self):
        pass

#--------LEARN MODE GUI FRAME--------# 
    def learn_frame(self):
        pass

if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()
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

        self.show_main()

#--------CLEANING FRAMES--------# 
    def frame_clear(self):
        for frame in self.frames.values():
            frame.grid_forget()

#--------MAIN GUI FRAME--------# 
    def show_main(self):
        self.frame_clear()

        self.frames['main'].grid(column=0, row=0, sticky="nsew")
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
                               command=self.show_encode)
        encode_button.grid(column=1,row=3)

        decode_button = Button(self.frames['main'],
                               text="Decode",
                               font=(FONT_NAME,15),
                               width=40,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.show_decode)
        decode_button.grid(column=1,row=4,pady=8)

        learn_button = Button(self.frames['main'],
                              text="Learn",
                              font=(FONT_NAME,15),
                              width=40,
                              bg=BUTTON_BACKGROUND,
                              fg='white',
                              command=self.show_learn)
        learn_button.grid(column=1,row=5)

#--------ENCODE GUI FRAME--------# 
    def show_encode(self):
        self.frame_clear()

        self.frames['encode'].grid(column=0, row=0, sticky="nsew")
        for i in range(0,15):  
            self.frames['encode'].grid_columnconfigure(i, weight=1,minsize=30)  
            if i < 7:  
                self.frames['encode'].grid_rowconfigure(i, weight=1,minsize=10)

        self.create_keyboard()

        back_button = Button(self.frames['encode'],
                               text="Back",
                               font=(FONT_NAME,10),
                               width=45,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.show_main)
        back_button.grid(column=1,row=7,columnspan=14,padx=5)

#--------ENCODE KEYBOARD SETUP--------#
    def create_keyboard(self):
        alphabet_dict = MorseLogic().alphabet_dict
        letters = list(alphabet_dict.keys())
        codes = list(alphabet_dict.values())
        column_n,row_n = 1,1

        for i in range(len(letters)):
            alphabet_button = Button(self.frames['encode'],
                                     text=f'{letters[i].upper()}\n{codes[i]}',
                                     font=(FONT_NAME,13),
                                     width=5,
                                     bg=BUTTON_BACKGROUND,
                                     fg='white')
            alphabet_button.grid(column=column_n, row=row_n, sticky='nsew',pady=1,padx=1)
            column_n += 1

            if column_n == 14:
                column_n = 1
                row_n += 1
#--------DECODE GUI FRAME--------# 
    def show_decode(self):
        self.frame_clear()
        self.frame_setup(self.frames['decode'])

#--------LEARN MODE GUI FRAME--------# 
    def show_learn(self):
        self.frame_clear()
        self.frame_setup(self.frames['learn'])

        label = Label(self.frames['learn'], text="Learn", font=("Arial", 16))
        label.grid(column=0, row=0, pady=20)

if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()


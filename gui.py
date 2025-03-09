from tkinter import *

#--------CONSTANTS--------# 
BACKGROUND = '#242424'
BUTTON_BACKGROUND = '#828282'
FONT_NAME = 'Chicago'
WINDOW_SIZE = "800x800"

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

        self.main()

    def frame_clear(self):
        for frame in self.frames.values():
            frame.grid_forget()

    def frame_setup(self, frame):
        frame.grid(column=0, row=0, sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)  
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

    def main(self):
        self.frame_clear()
        self.frame_setup(self.frames['main'])

        main_label = Label(self.frames['main'],text='Morse Code Converter',
                           font=(FONT_NAME,50,'bold'),
                           bg=BACKGROUND,
                           fg='white')
        main_label.grid(column=0,row=0,columnspan=3,padx=30,pady=(60,20))

        encode_button = Button(self.frames['main'],
                               text="Encode",
                               font=(FONT_NAME,15),
                               width=40,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.show_encode)
        encode_button.grid(column=1,row=1)

        decode_button = Button(self.frames['main'],
                               text="Decode",
                               font=(FONT_NAME,15),
                               width=40,
                               bg=BUTTON_BACKGROUND,
                               fg='white',
                               command=self.show_decode)
        decode_button.grid(column=1,row=2,pady=8)

        learn_button = Button(self.frames['main'],
                              text="Learn",
                              font=(FONT_NAME,15),
                              width=40,
                              bg=BUTTON_BACKGROUND,
                              fg='white',
                              command=self.show_learn)
        learn_button.grid(column=1,row=3)

    def show_encode(self):
        self.frame_clear()
        self.frame_setup(self.frames['encode'])

        self.frames['encode'].grid(column=0, row=0)

        label = Label(self.frames['encode'], text="Encode", font=("Arial", 16))
        label.grid(column=0, row=0, pady=20)

    def show_decode(self):
        self.frame_clear()
        self.frame_setup(self.frames['decode'])

        self.frames['decode'].grid(column=0, row=0)

        label = Label(self.frames['decode'], text="Decode", font=("Arial", 16))
        label.grid(column=0, row=0, pady=20)

    def show_learn(self):
        self.frame_clear()
        self.frame_setup(self.frames['learn'])

        self.frames['learn'].grid(column=0, row=0)

        label = Label(self.frames['learn'], text="Learn", font=("Arial", 16))
        label.grid(column=0, row=0, pady=20)

if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()


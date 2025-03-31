#---------------------------IMPORTS----------------------------# 
from tkinter import *
from config import *
from frames import MainFrame, EncodeFrame, LearnFrame

#--------------------------MORSE APP---------------------------# 
class MorseApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Morse Code Converter App")
        self.config(bg=BACKGROUND)
        self.geometry(WINDOW_SIZE)

        self.frames = {}
        for frame_class in (MainFrame, EncodeFrame, LearnFrame):
            frame = frame_class(self)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainFrame)

    def show_frame(self,frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == "__main__":
    morse_app = MorseApp()
    morse_app.mainloop()
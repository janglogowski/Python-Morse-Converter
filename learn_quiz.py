import random

class Learn():
    def ____init__(self):
        with open("highest_score.txt",'w+') as highest_score:
            self.highscore = highest_score.read()
            if self.highscore == '':
                self.highscore = 0
        self.score = 0

    def choose_type(self):
        type = random.randint(1,3)
        type_dict = {1:self.text_to_code(),
                     2:self.code_to_text(),
                     3:self.audio_to_code()}
        return type_dict[type]

    def text_to_code(self):
        pass

    def code_to_text(self):
        pass

    def audio_to_code(self):
        pass


l = Learn()
l.choose_type()
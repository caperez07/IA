from gtts import gTTS

import os

class TextToSpeech:
    def __init__(self, language='pt-br'):
        
        self.language = language

    def save(self, text):
        myobj = gTTS(text=text, lang=self.language, slow=False)
        myobj.save("answer.mp3")
        os.system("start answer.mp3")

# mytext = 'O Gabriel Medina é muito bom!'

# language = 'pt-br'

# myobj = gTTS(text=mytext, lang=language, slow=False)

# myobj.save("welcome.mp3")

# os.system("start welcome.mp3")
from gtts import gTTS

import os

class TextToSpeech:
    def __init__(self, text, language='pt-br'):
        self.text = text
        self.language = language

    def save(self):
        myobj = gTTS(text=self.text, lang=self.language, slow=False)
        myobj.save("welcome.mp3")
        os.system("start welcome.mp3")

# mytext = 'O Gabriel Medina é muito bom!'

# language = 'pt-br'

# myobj = gTTS(text=mytext, lang=language, slow=False)

# myobj.save("welcome.mp3")

# os.system("start welcome.mp3")
# from gtts import gTTS

from elevenlabs.client import ElevenLabs
from elevenlabs import play, save, stream, Voice, VoiceSettings

import os

client = ElevenLabs(api_key="sk_f366eab96a7243077e4fc0184bd51ec34cd4a48c322bbb40")

class TextToSpeech:
    def __init__(self, language='pt-br'):
        
        self.language = language

    # def save(self, text):
    #     myobj = gTTS(text=text, lang=self.language, slow=False)
    #     myobj.save("answer.mp3")
    #     os.system("start answer.mp3")
    
    def save(self, text):
        audio = client.generate(
        voice="River")
        play(audio)
        save(audio, "output.mp3")


# mytext = 'O Gabriel Medina é muito bom!'

# language = 'pt-br'

# myobj = gTTS(text=mytext, lang=language, slow=False)

# myobj.save("welcome.mp3")

# os.system("start welcome.mp3")
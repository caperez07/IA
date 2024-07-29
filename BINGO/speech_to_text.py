import speech_recognition as sr
import threading
import sounddevice as sd

class SpeechToText:
    def __init__(self):
        self.thread_limit = 3
        self.active_thread = 0
        self.mic = sr.Recognizer()
    
    def getAudio(self):
        with sr.Microphone(device_index=1) as source:
            self.mic.adjust_for_ambient_noise(source)
            # print('Fale alguma coisa:')

            try:
                audio = self.mic.listen(source)
                frase: str = self.mic.recognize_google(audio, language='pt-BR')

                if frase.lower().__contains__('bingo'):
                    # print(frase)
                    return frase
                else:
                    pass
            except sr.UnknownValueError:
                # print('Não entendi o que você disse.')
                pass
            except sr.RequestError as e:
                print(f'Erro na requisição: {e}')
            finally:
                self.active_thread -= 1



    def Begin(self):
        # while True:
        #     if self.active_thread < self.thread_limit:
        #         self.active_thread += 1
        #         threading.Thread(target=self.checkIfBingo).start()
        
        # while self.active_thread < self.thread_limit:
        #     self.active_thread += 1
        #     threading.Thread(target=self.getAudio).start()

        while True:
            self.getAudio()

if __name__ == '__main__':
    print(sd.query_devices())
    # SpeechToText().Begin()
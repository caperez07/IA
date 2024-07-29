from chatbot import ChatBot
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech

speech = SpeechToText()
chatbot = ChatBot()
text = TextToSpeech()

def main():
    print("Para sair, diga 'bingo, sair'.")
    print('Fale alguma coisa:')
    while True:
        frase = speech.getAudio()
        if frase:
            print(f'Você: {frase}')
            if 'bingo sair' in frase.lower():
                break
            elif 'bingo' in frase.lower():
                resposta = chatbot.enviar_mensagem(frase)
                text.save(resposta)
                print('Chatbot: ', resposta)
                print('Fale alguma coisa:')

if __name__ == '__main__':
    main()
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
        # TODO: pegar microfone 100% e observar audio
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

# continuar conversa se tiver a ver com o que foi dito

if __name__ == '__main__':
    main()
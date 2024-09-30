from chatbot import ChatBot
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from rag.rag import Rag

speech = SpeechToText()
# chatbot = ChatBot()
rag_agent = Rag()
text = TextToSpeech()

# def main():
#     print("Para sair, diga 'bingo, sair'.")
#     print('Fale alguma coisa:')
#     while True:
#         # TODO: pegar microfone 100% e observar audio
#         frase = speech.getAudio()
#         if frase:
#             print(f'Você: {frase}')
#             if 'bingo sair' in frase.lower():
#                 break
#             elif 'bingo' in frase.lower():
#                 # resposta = chatbot.enviar_mensagem(frase)
#                 resposta = rag_agent.setup_agent(frase)
#                 text.save(resposta['output'])
#                 print('Bingo: ', resposta['output'])
#                 print('Fale alguma coisa:')

def main():
    print("Para sair, diga 'bingo, sair'.")
    print('Fale alguma coisa:')
    while True:
        frase = input("Você: ")
        if frase:
            print(f'Você: {frase}')
            if 'bingo sair' in frase.lower():
                break

            resposta = rag_agent.setup_agent(frase)
            print('Bingo: ', resposta['output'])
            print('Fale alguma coisa:')
                
    

# continuar conversa se tiver a ver com o que foi dito

if __name__ == '__main__':
    main()
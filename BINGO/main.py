# from chatbot import ChatBot
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

# def main():
#     print("Para sair, diga 'bingo, sair'.")
#     print('Fale alguma coisa:')
#     while True:
#         frase = input("Você: ")
#         if frase:
#             # print(f'Você: {frase}')
#             if 'bingo sair' in frase.lower():
#                 break

#             resposta = rag_agent.setup_agent(frase)
#             print('Bingo: ', resposta['output'])

# def main():
#     print("Para sair, diga 'bingo, sair'.")
#     print('Fale alguma coisa:')
#     while True:
#         frase = input("Você: ")
#         if frase:
#             # print(f'Você: {frase}')
#             if 'bingo sair' in frase.lower():
#                 break
#             elif frase.startswith('bingo'):
#                 resposta = rag_agent.setup_agent(frase)
#                 print('Bingo: ', resposta['output'])

import threading

# Variável para controlar o estado de timeout
timeout_ocorrido = False
temporizador_ativo = False  # Variável para verificar se o timer já foi ativado

def resetar_timeout():
    """Função chamada após 20 segundos sem interação."""
    global timeout_ocorrido, temporizador_ativo
    timeout_ocorrido = True
    temporizador_ativo = False  # Desativa o temporizador
    print("----- Nenhuma interação em 20 segundos. Resetando... -----")

def main():
    global timeout_ocorrido, temporizador_ativo
    print("Para sair, diga 'bingo, sair'.")
    print('Fale alguma coisa:')
    
    timer = None  # Referência ao timer para poder cancelar
    
    while True:
        frase = input("Você: ")
        
        if frase:
            # Se o temporizador ainda não foi ativado, espera por "bingo"
            if not temporizador_ativo and frase.lower().startswith('bingo'):
                temporizador_ativo = True
                print("----- Temporizador iniciado. -----")
                timer = threading.Timer(50.0, resetar_timeout)  # Iniciar o temporizador
                timer.start()
                resposta = rag_agent.setup_agent(frase)
                print('Bingo: ', resposta['output'])
            
            # Se o temporizador estiver ativo e o timeout ainda não ocorreu
            elif temporizador_ativo and not timeout_ocorrido:
                if timer:  # Cancela o timer e reinicia o tempo
                    timer.cancel()
                timer = threading.Timer(50.0, resetar_timeout)  # Reiniciar o temporizador
                timer.start()
                print("----- Temporizador reiniciado. -----")
                
                resposta = rag_agent.setup_agent(frase)
                print('Bingo: ', resposta['output'])

            # Se o timeout ocorreu, só responde se a frase começar com "bingo"
            if timeout_ocorrido:
                if frase.lower().startswith('bingo'):
                    # Resetar o estado e iniciar temporizador novamente
                    timeout_ocorrido = False
                    temporizador_ativo = True
                    print("----- Temporizador iniciado novamente. -----")
                    if timer:  # Cancela o timer anterior, se existir
                        timer.cancel()

                    timer = threading.Timer(50.0, resetar_timeout)  # Reiniciar o timer
                    timer.start()
                    resposta = rag_agent.setup_agent(frase)
                    print('Bingo: ', resposta['output'])
                else:
                    # print("O tempo esgotou. Aguarde 'bingo' para continuar.")
                    continue  # Ignora qualquer frase sem "bingo" após o timeout
            
            # Se o usuário quiser sair
            if 'bingo sair' in frase.lower():
                if timer:  # Se houver um timer ativo, cancela
                    timer.cancel()
                break
            

# continuar conversa se tiver a ver com o que foi dito

if __name__ == '__main__':
    main()
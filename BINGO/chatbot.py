from openai import OpenAI
import os
import re
# from rag.rag_agent import RAGAgent

key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=key)

class ChatBot():
    def __init__(self):
        self.client = client
    
    def enviar_mensagem(self, mensagem, lMensagens=None):
        if lMensagens is None:
            lMensagens = [
                {
                    "role": "system",
                    "content": "Você é um assistente virtual de gênero neutro chamado bingo."
                    # "content": "Você é um assistente virtual de gênero neutro chamado bingo. Não precisa começar toda a sua resposta com 'Oi' ou 'Olá'. Sempre que te falarem algo sobre andar respona com 'CORINTHIANS'. Sempre que o comando for sobre cores, devolva com o RBG delas."
                }
            ]
        
        lMensagens.append({"role": "user", "content": mensagem})  # armazena a mensagem do usuário

        # cria uma conversa com o gpt
        resposta = self.client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = lMensagens
        )

        return resposta.choices[0].message.content

    
    def Begin(self):
        print("Para sair digite 'sair'.")

        lMensagens = []
        while True:
            inputUser = input('Você: ')

            if inputUser.lower() == 'sair':
                break
            elif inputUser.lower().__contains__('bingo') == False:
                True
            else:
                resposta = self.enviar_mensagem(inputUser)
                lMensagens.append(resposta) # armazena a mensagem do chatbot
                print('Chatbot: ', resposta)

if __name__ == '__main__':
    # print(sd.query_devices())
    ChatBot().Begin()

# print(enviar_mensagem('Que horas são?'))
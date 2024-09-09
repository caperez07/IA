from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_community.llms.ollama import Ollama
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain import hub
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,
)
from embedding_function import get_embedding_function

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Você é um assistente virtual que ajuda a responder perguntas sobre música.
Use o contexto a seguir para responder as perguntas. Seja o mais detalhado possível.
Se você não sabe uma resposta, diga "Eu não sei".

Contexto: {context}

Pergunta: {input}
"""

class RAGAgent:
    def __init__(self):
        self.agent_executor = self.setup_agent()

    def setup_agent(self):
        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["context"],
                template=PROMPT_TEMPLATE,
            )
        )

        # human_prompt = HumanMessagePromptTemplate(
        #     prompt=PromptTemplate(
        #         input_variables=["question"],
        #         template="{question}",
        #     )
        # )
        human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["input"],
                template="{input}",
            )
        )
        messages = [system_prompt, human_prompt]

        prompt_template = ChatPromptTemplate(
            input_variables=["context", "input"],
            messages=messages,
        )

        chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        output_parser = StrOutputParser()  # formata a resposta

        # Preparando o db
        embedding_function = get_embedding_function()
        db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=embedding_function
        )

        results = db.as_retriever(k=10)

        review_chain = (
            {"context": results}
            | prompt_template
            | chat_model
            | output_parser
        )

        tools = [
            Tool(
                name="Music",
                func=review_chain.invoke,
                description="""
                Útil quando você precisa responder qualquer coisa sobre música em geral.
                Não é útil para responder a perguntas sobre concertos específicos ou músicas pouco conhecidas.
                Passe a pergunta inteira como entrada para a ferramenta.
                """,
            ),
            # TODO: ferramentas para funcoes fora do rag
        ]

        agent_prompt = hub.pull("hwchase17/openai-functions-agent")

        agent_chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        agent = create_openai_functions_agent(
            llm=agent_chat_model,
            prompt=agent_prompt,
            tools=tools,
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            return_intermediate_steps=True,  # permite ver o passo a passo do agente
            verbose=True,  # permite ver o pensamento do agente
        )

        return agent_executor

    def invoke(self, question):
        return self.agent_executor.invoke({"input": question})
    
def chat():
    agent = RAGAgent()

    print("Para sair, digite 'sair'.")
    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            print("Encerrando o chatbot.")
            break

        response = agent.invoke(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chat()



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
from corinthians import corinthians
from langchain.tools import StructuredTool

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
You are an artificial inteligence that helps answering various questions, but has a special knowledge about music.
Use the following context to answer the questions. You don't need to give very long answers, summarize with important information.
If you don't know an answer, say "I don't know".

Context: {context}

Question: {question}
"""

class RAGAgent:
    def __init__(self):
        self.music_agent_executor = self.setup_music_agent()

    def setup_music_agent(self):
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
            input_variables=["context", "question"],
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
            {"context": results, "question": RunnablePassthrough()}
            | prompt_template
            | chat_model
            | output_parser
        )

        tools = [
            Tool(
                name="Music",
                func=review_chain.invoke,
                description="""
                Useful when you need to answer anything about music in general.
                Not useful to answer questions about specific concerts or lesser-known songs.
                Pass the entire question as input to the tool.
                """,
            ),
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
            return_intermediate_steps=False,  # permite ver o passo a passo do agente
            verbose=False,  # permite ver o pensamento do agente
        )

        return agent_executor
        # return review_chain
    
    def handle_general_question(self, question):
        prompt = f"Você é um chatbot que responde a perguntas gerais. Responda apenas com 'Corinthians'. Pergunta: {question}."
        response = self.general_chat_model.invoke(prompt)
        return response

    def invokeAgent(self, question):
        return self.music_agent_executor.invoke({"input": question})
    
def chat():
    agent = RAGAgent()

    print("Para sair, digite 'sair'.")
    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            print("Encerrando o chatbot.")
            break

        response = agent.invokeAgent(user_input)
        print(f"Chatbot: {response["output"]}")

if __name__ == "__main__":
    chat()



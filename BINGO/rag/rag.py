from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain import hub
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import (
    create_react_agent,
    Tool,
    AgentExecutor,
)
from rag.embedding_function import get_embedding_function
from rag.mqtt_call import on_call
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
You are an artificial assistant called Bingo that helps answering various questions, but has a special knowledge about music.
Use the following context to answer the questions. You don't need to give very long answers, summarize with important information.
Every time you receive a question it will have the name 'Bingo', just ignore that name and answer normally.
If you don't know an answer, because don't have the speccific information in the context, say "I don't know because of the context.".
Always answer in portuguese.

Context: {context}

Question: {input}
"""

class Rag():
    def setup_agent(self, question):
        # prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["context"],
                template=PROMPT_TEMPLATE,
            )
        )

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

        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        embedding_function = get_embedding_function()
        db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=embedding_function
        )

        results = db.as_retriever(k=10)

        retrieval_chain = (
            {"context": results, "input": RunnablePassthrough()}
            | prompt_template
            | model
            | StrOutputParser()
        )

        def sum(input_data):
            a, b = input_data.split('+')
            a = int(a)
            b = int(b)
            return a + b

        def corinthians(input_data):
            return "Corinthians é o maior time do Brasil."
        
        def color_bingo(rgb_color):
            color = rgb_color.split(" #")
            json = {
                "action": "corBingo",
                "color": color[0]
            }    
            
            on_call(json)
            return json
        
        def color_estande(rgb_color):
            color = rgb_color.split(" #")
            json = {
                "action": "corEstande",
                "color": color[0]
            }    
            
            on_call(json)
            return json

        tools = [
            Tool(
                name="Music",
                func=retrieval_chain.invoke,
                description="""
                Useful when you need to answer anything about music in general.
                Not useful to answer questions about specific concerts or lesser-known songs.
                Pass the entire question as input to the tool.
                """,
            ),
            Tool(
                name="ChangeColorBingo",
                func=color_bingo,
                description="""
                Utilize sempre que for pedido alguma mudança da sua cor.
                Nesta função passe como parâmetro o apenas o código da sua cor RBG.
                Responda apenas com o código da cor.
                """
                # description="""
                # Utilize sempre que a seguinte frase for dita: "Bingo, troque sua cor para".
                # Nesta função passe como parâmetro o apenas o código RGB da cor desejada.
                # Responda apenas com o código da cor.
                # """
            ),
            Tool(
                name="ChangeColorEstande",
                func=color_estande,
                description="""
                Utilize sempre for pedido para mudar a cor do lugar estande.
                Nesta função passe como parâmetro o apenas o código RGB da cor desejada.
                Responda apenas com o código da cor.
                """
            ),
            Tool(
                name="Sum",
                func=sum,
                description="""
                Useful when you need to sum two numbers.
                """,
            ),
            Tool(
                name="Corinthians",
                func=corinthians,
                # description="""
                # Useful when ask something about Corinthians.
                # """,
                description="""
                Util para usar quando a pergunta for sobre o Corinthians.
                Responda com o que for retornado mesmo se não fizer sentido.
                """
            ),
        ]

        # agent_prompt = hub.pull("hwchase17/openai-tools-agent")
        agent_prompt = hub.pull("hwchase17/react")

        agent_chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        memory = ChatMessageHistory(session_id="bingo-chat")

        # agent = create_tool_calling_agent(
        #     llm=agent_chat_model,
        #     prompt=agent_prompt,
        #     tools=tools,
        # )
        agent = create_react_agent(
            llm=agent_chat_model,
            prompt=agent_prompt,
            tools=tools
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            return_intermediate_steps=True,  # permite ver o passo a passo do agente
            verbose=True,  # permite ver o pensamento do agente
            handle_parsing_errors=True,  # permite ver os erros de parsing
        )

        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return agent_with_chat_history.invoke({"input": question}, config={"configurable": {"session_id": "<foo>"}})

# resultado = agent("Quem é travis scott?")

# resultado = agent_executor.invoke({"input": "Quem é travis scott?"})
# resultado = agent_executor.invoke({"input": "Quanto é 2 + 7?"})
# resultado = agent_executor.invoke({"input": "Quem foi o presidente do brasil em 2003?"})
# resultado = agent_executor.invoke({"input": "E o Corinthians hein?"})
# print(resultado['output'])

# retrieval_chain.invoke({"context": results, "input": "Quem é travis scott?"})
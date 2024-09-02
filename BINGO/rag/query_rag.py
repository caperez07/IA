import argparse
from embedding_function import get_embedding_function
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

CHROMA_PATH = "chroma"

# PROMPT_TEMPLATE = """
# Answer the question based only on the following context:
# {context}

# ---
# Answer the question based on the above context: {question}
# """

PROMPT_TEMPLATE = """
Responda a pergunta baseado apenas no seguinte contexto:
{context}

---
Responda a pergunta baseado no contexto acima: {question}
"""

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)
    # rag()

def query_rag(query_txt: str):
    # preparando o db
    embedding_function = get_embedding_function()
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_function
    )

    results = db.similarity_search_with_score(query_txt, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_txt)

    model = Ollama(model="llama3")
    response_text = model.invoke(prompt)
    # print(response_text)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

# def rag():
#     system_prompt = SystemMessagePromptTemplate(
#         prompt=PromptTemplate(
#             input_variables=["context"],
#             template=PROMPT_TEMPLATE,
#         )
#     )

#     human_prompt = HumanMessagePromptTemplate(
#         prompt=PromptTemplate(
#             input_variables=["question"],
#             template="{question}",
#         )
#     )
#     messages = [system_prompt, human_prompt]

#     prompt_template = ChatPromptTemplate(
#         input_variables=["context", "question"],
#         messages=messages,
#     )

#     chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

#     output_parser = StrOutputParser() # fromata a responsta

#     # preparando o db
#     embedding_function = get_embedding_function()
#     db = Chroma(
#         persist_directory=CHROMA_PATH, embedding_function=embedding_function
#     )

#     results = db.as_retriever(k=10)

#     review_chain = (
#         {"context": results, "question": RunnablePassthrough()}
#         | prompt_template
#         | chat_model
#         | output_parser
#     )

if __name__ == "__main__":
    main()
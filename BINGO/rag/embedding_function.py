# from langchain_community.embeddings.bedrock import BedrockEmbeddings
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

def get_embedding_function():
    embeddings = OpenAIEmbeddings() # ver modelo mais barato
    return embeddings
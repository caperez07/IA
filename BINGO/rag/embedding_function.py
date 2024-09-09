# from langchain_community.embeddings.bedrock import BedrockEmbeddings
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

def get_embedding_function():
    # embeddings = BedrockEmbeddings( # langchain documentation para diferentes embeddings
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    # embeddings = OllamaEmbeddings(model="llama3")
    embeddings = OpenAIEmbeddings()
    return embeddings
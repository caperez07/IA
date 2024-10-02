# from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
# from langchain_openai import OpenAIEmbeddings
# from sentence_transformers import SentenceTransformer

def get_embedding_function():
    # embeddings = OpenAIEmbeddings() # ver modelo mais barato
    embeddings = OllamaEmbeddings(model="llama3")
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )

    # encoder = SentenceTransformer('all-MiniLM-L6-v2')
    # embeddings = encoder.encode(chunks)
    return embeddings
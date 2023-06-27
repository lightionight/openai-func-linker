import os 
import openai

def convertTextToVector(
        context
):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(
        model = "text-embedding-ada-002",
        input = context
    )
    return response['data'][0]['embedding']


import os 
from dotenv import load_dotenv
from chunck import chunck
from openai import OpenAI

def embed():

    load_dotenv()
    chuncks = chunck()
    client = OpenAI(api_key=os.getenv("API_KEY"))
    vectors = []

    for chunck_item in chuncks:

        response = client.embeddings.create(
            input = chunck_item["text"],
            model = os.getenv("MODEL")
        )
        vector = response.data[0].embedding

        vectors.append({"vector" : vector, "text" : chunck_item["text"], "source" : chunck_item["file_path"]})
    
    return vectors

vectors = embed()
print(vectors)






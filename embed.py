import os 
import psycopg2
from dotenv import load_dotenv
from chunck import chunck
from openai import OpenAI

def embed():

    load_dotenv()
    chuncks = chunck()
    client = OpenAI(api_key=os.getenv("API_KEY"))

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    curr = conn.cursor()
    for chunck_item in chuncks:

        response = client.embeddings.create(
            input = chunck_item["text"],
            model = os.getenv("MODEL")
        )
        vector = response.data[0].embedding

        curr.execute(
            "INSERT INTO chunks (text, source, embedding) VALUES (%s, %s, %s)",
            (chunck_item["text"], chunck_item["file_path"], str(vector))
        )

    conn.commit()
    curr.close()
    conn.close()
    
    print(f"Inserted {len(chuncks)} embeddings into the database.")

embed()






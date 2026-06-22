import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

def search(query):
    load_dotenv()
    
    client = OpenAI(api_key=os.getenv("API_KEY"))

    # Embed the query
    query_vector_response = client.embeddings.create(
            input = query,
            model = os.getenv("MODEL")
        )
    query_vector = query_vector_response.data[0].embedding

    # Connect to the database (Docker in this case)
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    curr = conn.cursor()

    curr.execute("SELECT text, source, 1 - (embedding <=> %s) AS similarity FROM chunks ORDER BY embedding <=> %s LIMIT 5", (str(query_vector), str(query_vector)))
    relevant_chunks = curr.fetchall()

    curr.close()
    conn.close()

    print(f"Top relevant chunks for the query '{query}':")

    for chunk in relevant_chunks:
        print(f"Source: {chunk[1]}, Similarity Score: {chunk[2]}\n")
        print(f"Text Snipet: {chunk[0][:100]}\n")

    return relevant_chunks





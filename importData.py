import json
import psycopg2
from dotenv import load_dotenv
import os

with open("dataCrawler.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("Documents in JSON:", len(data))

load_dotenv()

password = os.getenv("POSTGRES_PASSWORD")

connection = psycopg2.connect(
    host="localhost",
    database="Custom_Search_Engine",
    user="postgres",
    password=password
)

cursor = connection.cursor()

print("Database connected!")

for document in data:
    cursor.execute(
        """
    INSERT INTO documents (url, title, snippet)
    VALUES (%s, %s, %s)
    ON CONFLICT (url) DO UPDATE
    SET title = EXCLUDED.title,
        snippet = EXCLUDED.snippet
    RETURNING document_id
    """,
        (
            document["url"],
            document["title"],
            document["snippet"]
        )
    )

    documentId = cursor.fetchone()[0]

    print("\nDocument:", document["title"])
    print("Document ID:", documentId)

    for word, frequency in document["word_counts"].items():

        cursor.execute(
            """
            INSERT INTO terms (word)
            VALUES (%s)
            ON CONFLICT (word) DO UPDATE
            SET word = EXCLUDED.word
            RETURNING term_id
            """,
            (word,)
        )

        termId = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO docTermFrequency
                (document_id, term_id, frequency)
            VALUES
                (%s, %s, %s)
            ON CONFLICT (document_id, term_id)
            DO UPDATE SET frequency = EXCLUDED.frequency
            """,
            (
                documentId,
                termId,
                frequency
            )
        )

connection.commit()
cursor.close()
connection.close()

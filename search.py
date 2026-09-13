import psycopg2
from dotenv import load_dotenv
import os

query = input("Search: ")

queryTokens = query.lower().split()

if not queryTokens:
    print("Please enter a search query.")
    exit()

load_dotenv()

password = os.getenv("POSTGRES_PASSWORD")

connection = psycopg2.connect(
    host="localhost",
    database="Custom_Search_Engine",
    user="postgres",
    password=password
)

cursor = connection.cursor()

placeholders = ", ".join(["%s"] * len(queryTokens))

cursor.execute(
    f"""
    WITH tf_data AS (
        SELECT
            documents.document_id,
            documents.title,
            documents.url,
            terms.word,
            docTermFrequency.frequency,

            docTermFrequency.frequency::decimal /
            SUM(docTermFrequency.frequency) OVER (
                PARTITION BY docTermFrequency.document_id
            ) AS tf

        FROM docTermFrequency

        JOIN documents
            ON documents.document_id = docTermFrequency.document_id

        JOIN terms
            ON terms.term_id = docTermFrequency.term_id
    ),

    idf_data AS (
        SELECT
            terms.word,

            LOG(
                (SELECT COUNT(*) FROM documents)::decimal /
                COUNT(DISTINCT docTermFrequency.document_id)
            ) AS idf

        FROM docTermFrequency

        JOIN terms
            ON terms.term_id = docTermFrequency.term_id

        GROUP BY terms.word
    ),

    tfidf_data AS (
        SELECT
            tf_data.document_id,
            tf_data.title,
            tf_data.url,
            tf_data.word,
            tf_data.tf * idf_data.idf AS tf_idf

        FROM tf_data

        JOIN idf_data
            ON tf_data.word = idf_data.word
    )

    SELECT
        document_id,
        title,
        url,
        SUM(tf_idf) AS score
    FROM tfidf_data
    WHERE word IN ({placeholders})
    GROUP BY document_id, title, url
    HAVING COUNT(DISTINCT word) = %s
    ORDER BY score DESC;
    """,
    tuple(queryTokens) + (len(queryTokens),)
)

results = cursor.fetchall()

if not results:
    print("No Results Found!")
else:
    for result in results:
        documentId, title, url, score = result

        print(f"\n{title}")
        print(url)
        print(f"Score: {float(score):.5f}")

cursor.close()
connection.close()

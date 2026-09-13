from flask import Flask, render_template, request, redirect
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


def get_connection():
    password = os.getenv("POSTGRES_PASSWORD")
    return psycopg2.connect(
        host="localhost",
        database="Custom_Search_Engine",
        user="postgres",
        password=password
    )


@app.route('/')
def home():
    return render_template('HomePageUI.html')


@app.route('/search')
def search():
    user_query = request.args.get('query', '').strip()
    action = request.args.get('action', 'search')

    if not user_query:
        return render_template('ResultsUI.html', query=user_query, results=[])

    queryTokens = user_query.lower().split()

    connection = get_connection()
    cursor = connection.cursor()

    placeholders = ", ".join(["%s"] * len(queryTokens))

    cursor.execute(
        f"""
        WITH tf_data AS (
            SELECT
                documents.document_id,
                documents.title,
                documents.snippet,
                documents.url,
                terms.word,
                docTermFrequency.frequency,
                docTermFrequency.frequency::decimal /
                SUM(docTermFrequency.frequency) OVER (
                    PARTITION BY docTermFrequency.document_id
                ) AS tf
            FROM docTermFrequency
            JOIN documents ON documents.document_id = docTermFrequency.document_id
            JOIN terms ON terms.term_id = docTermFrequency.term_id
        ),
        idf_data AS (
            SELECT
                terms.word,
                LOG(
                    (SELECT COUNT(*) FROM documents)::decimal /
                    COUNT(DISTINCT docTermFrequency.document_id)
                ) AS idf
            FROM docTermFrequency
            JOIN terms ON terms.term_id = docTermFrequency.term_id
            GROUP BY terms.word
        ),
        tfidf_data AS (
            SELECT
                tf_data.document_id,
                tf_data.title,
                tf_data.snippet,
                tf_data.url,
                tf_data.word,
                tf_data.tf * idf_data.idf AS tf_idf
            FROM tf_data
            JOIN idf_data ON tf_data.word = idf_data.word
        )
        SELECT
            document_id,
            title,
            snippet,
            url,
            SUM(tf_idf) AS score
        FROM tfidf_data
        WHERE word IN ({placeholders})
        GROUP BY document_id, title, snippet, url
        HAVING COUNT(DISTINCT word) = %s
        ORDER BY score DESC;
        """,
        tuple(queryTokens) + (len(queryTokens),)
    )

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    if action == 'lucky' and rows:
        top_result_url = rows[0][3]
        return redirect(top_result_url)

    results = []
    for document_id, title, snippet, url, score in rows:
        results.append({
            "title": title,
            "snippet": snippet,
            "url": url,
            "score": float(score)
        })

    return render_template('ResultsUI.html', query=user_query, results=results)


if __name__ == '__main__':
    app.run(debug=True)

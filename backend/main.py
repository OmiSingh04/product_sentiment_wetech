import os
from flask import Flask, request, jsonify
import mysql.connector
import boto3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    password=os.getenv("DB_PASSWORD"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)

comprehend = boto3.client('comprehend', region_name='us-east-1')

def analyze_sentiment(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    scores = response['SentimentScore']
    return sentiment, scores


@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    product_id = data['product_id']
    rating = data['rating']
    comment = data['comment']

    # Insert new review
    cursor.execute(
        "INSERT INTO reviews (product_id, rating, comment) VALUES (%s, %s, %s)",
        (product_id, rating, comment)
    )
    db.commit()
    review_id = cursor.lastrowid

    # Step 1: Get total number of reviews for this product
    cursor.execute("SELECT COUNT(*) AS count FROM reviews WHERE product_id=%s", (product_id,))
    count = cursor.fetchone()['count']

    # Step 2: If count % 100 == 0, do batch sentiment
    if count % 50 == 0:
        #TODO: what is this query about?
        cursor.execute("SELECT comment FROM reviews WHERE product_id=%s ORDER BY review_id DESC LIMIT 100", (product_id,))
        recent_reviews = [r['comment'] for r in cursor.fetchall()]
        combined_text = ",\n".join(recent_reviews)

        sentiment, scores = analyze_sentiment(combined_text)

        # Store sentiment results in a separate table (one row per product batch)
        cursor.execute("""
                INSERT INTO product_sentiments 
                (product_id, overall_sentiment, positive_score, negative_score, neutral_score, mixed_score)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                overall_sentiment=VALUES(overall_sentiment),
                positive_score=VALUES(positive_score),
                negative_score=VALUES(negative_score),
                neutral_score=VALUES(neutral_score),
                mixed_score=VALUES(mixed_score),
                created_at=NOW()
            """, 
        (product_id, sentiment, scores['Positive'], scores['Negative'], scores['Neutral'], scores['Mixed']))
        db.commit()

    return jsonify({"message": "Review added", "review_id": review_id})

if __name__ == '__main__':
    app.run(debug=True)

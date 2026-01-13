import os
from flask import Flask, request, jsonify
import mysql.connector
import boto3
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        autocommit=True
    )

comprehend = boto3.client("comprehend", region_name="us-east-1")

def analyze_sentiment(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"], response["SentimentScore"]

@app.route("/add_review", methods=["POST"])
def add_review():
    data = request.json
    product_id = data["product_id"]
    rating = data["rating"]
    comment = data["comment"]

    with get_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "INSERT INTO reviews (product_id, rating, comment) VALUES (%s, %s, %s)",
                (product_id, rating, comment)
            )
            review_id = cursor.lastrowid

            cursor.execute(
                "SELECT COUNT(*) AS count FROM reviews WHERE product_id=%s",
                (product_id,)
            )
            count = cursor.fetchone()["count"]

            if count % 50 == 0:
                cursor.execute(
                    """
                    SELECT comment FROM reviews
                    WHERE product_id=%s
                    ORDER BY review_id DESC
                    LIMIT 50
                    """,
                    (product_id,)
                )
                comments = [r["comment"] for r in cursor.fetchall()]
                combined = ", ".join(comments)

                sentiment, scores = analyze_sentiment(combined)

                cursor.execute(
                    """
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
                    (
                        product_id,
                        sentiment,
                        scores["Positive"],
                        scores["Negative"],
                        scores["Neutral"],
                        scores["Mixed"],
                    )
                )

    return jsonify({"message": "Review added", "review_id": review_id})

@app.route("/api/categories")
def get_categories():
    with get_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT category_id AS id, name FROM categories")
            return jsonify(cursor.fetchall())

@app.route("/api/products")
def products_by_category():
    category_id = request.args.get("category_id")
    with get_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT product_id AS id, name FROM products WHERE category_id=%s",
                (category_id,)
            )
            return jsonify(cursor.fetchall())

@app.route("/api/products/<int:pid>")
def product(pid):
    with get_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT product_id AS id, name, description, price
                FROM products
                WHERE product_id=%s
                """,
                (pid,)
            )
            return jsonify(cursor.fetchone())

@app.route("/api/products/<int:pid>/reviews")
def reviews(pid):
    with get_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT rating, comment, created_at
                FROM reviews
                WHERE product_id=%s
                ORDER BY created_at DESC
                """,
                (pid,)
            )
            return jsonify(cursor.fetchall())

@app.route("/api/products/search")
def search_products():
    q = request.args.get("q")
    with get_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT product_id AS id, name FROM products WHERE name LIKE %s",
                (f"%{q}%",)
            )
            return jsonify(cursor.fetchall())


@app.route("/api/products/<int:pid>/sentiment")
def product_sentiment(pid):
    with get_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT overall_sentiment, positive_score, negative_score, neutral_score, mixed_score, created_at
                FROM product_sentiments
                WHERE product_id = %s
                """,
                (pid,)
            )
            sentiment = cursor.fetchone()
            
            if sentiment:
                return jsonify(sentiment)
            else:
                # No sentiment available for this product yet
                return jsonify({"message": "No sentiment data available"}), 404



if __name__ == "__main__":
    app.run(debug=True)
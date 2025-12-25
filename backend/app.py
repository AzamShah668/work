from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import random

app = Flask(__name__)
CORS(app)  # <-- This allows all origins

def get_connection():
    return psycopg2.connect(
        host="db",
        database="duadb",
        user="postgres",
        password="rootpass"
    )

@app.route("/dua")
def get_dua():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select dua_text from duas;")
    duas = cur.fetchall()
    cur.close()
    conn.close()

    dua = random.choice(duas)[0]
    return jsonify({"dua": dua})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


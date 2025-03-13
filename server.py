import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load database URL from Render
DATABASE_URL = os.getenv("DATABASE_URL")

# Convert "postgres://" to "postgresql://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 🟢 Test Database Connection
@app.route('/test_db')
def test_db():
    try:
        with db.engine.connect() as connection:
            connection.execute("SELECT 1")
        return jsonify({"message": "Database connected successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Start Flask App
if name == "__main__":
    app.run(debug=True)
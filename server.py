import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ Load the DATABASE_URL from Render environment variables
DATABASE_URL = os.getenv("DATABASE_URL")  # Fetch from environment variables

# ✅ Convert "postgres://" to "postgresql://" (Render uses an outdated format)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Make sure you added it in Render's environment variables.")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ✅ Test route to check database connection
@app.route('/test_db')
def test_db():
    try:
        with db.engine.connect() as connection:
            return {"message": "Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}

if name == "__main__":
    app.run(debug=True)
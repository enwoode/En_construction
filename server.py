import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load database URL from Render environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Convert "postgres://" to "postgresql://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 🟢 Register Customer
@app.route('/register_customer', methods=['POST'])
def register_customer():
    data = request.json
    phone = data['phone']

    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM customers WHERE phone = %s", (phone,))
        existing_customer = result.fetchone()
        
        if existing_customer:
            return jsonify({"message": "Customer already exists"}), 400

        sql = "INSERT INTO customers (fname, sname, address, phone) VALUES (%s, %s, %s, %s)"
        values = (data['fname'], data['sname'], data['address'], phone)
        connection.execute(sql, values)
        connection.commit()

    return jsonify({"message": "Customer registered successfully"}), 201

# 🟢 Get All Customers
@app.route('/customers', methods=['GET'])
def get_customers():
    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM customers")
        customers = result.fetchall()
    return jsonify([dict(row) for row in customers])

# ✅ Run Flask App
if name == "__main__":
    app.run(debug=True)
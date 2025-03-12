from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)  # ✅ Fix: Use name instead of main

# Connect to Postgres Database
db = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="newpassword",
    database="en_construction"
)
cursor = db.cursor()

# 🟢 Register Customer
@app.route('/register_customer', methods=['POST'])
def register_customer():
    data = request.json
    phone = data['phone']

    # Check if customer already exists
    cursor.execute("SELECT * FROM customers WHERE phone = %s", (phone,))
    existing_customer = cursor.fetchone()
    if existing_customer:
        return jsonify({"message": "Customer already exists"}), 400

    # Insert new customer
    sql = "INSERT INTO customers (fname, sname, address, phone) VALUES (%s, %s, %s, %s)"
    values = (data['fname'], data['sname'], data['address'], phone)
    cursor.execute(sql, values)
    db.commit()
    
    return jsonify({"message": "Customer registered successfully"}), 201

# 🟢 Register Equipment
@app.route('/register_equipment', methods=['POST'])
def register_equipment():
    data = request.json
    sql = "INSERT INTO equipment (ename, type, dateAdded) VALUES (%s, %s, NOW())"
    values = (data['ename'], data['type'])
    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Equipment registered successfully"}), 201

# 🟢 Hire Out Equipment
@app.route('/hire_equipment', methods=['POST'])
def hire_equipment():
    data = request.json
    sql = "INSERT INTO transactions (custId, eId, dateHired) VALUES (%s, %s, NOW())"
    values = (data['custId'], data['eId'])
    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Equipment hired out"}), 201

# 🟢 Return Equipment
@app.route('/return_equipment', methods=['POST'])
def return_equipment():
    data = request.json
    sql = "UPDATE transactions SET dateReturn = NOW() WHERE eId = %s AND custId = %s AND dateReturn IS NULL"
    values = (data['eId'], data['custId'])
    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Equipment returned"}), 200

# 🟢 Get All Customers
@app.route('/customers', methods=['GET'])
def get_customers():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    return jsonify(customers)

# 🟢 Get Available Equipment
@app.route('/equipment', methods=['GET'])
def get_equipment():
    cursor.execute("SELECT * FROM equipment")
    equipment = cursor.fetchall()
    return jsonify(equipment)

# ✅ Corrected main check
if __name__ == "__main__":
    app.run(debug=True)
    
    import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load database URL from Render
DATABASE_URL = os.getenv("DATABASE_URL")  # Fetch from environment variables

# Convert "postgres://" to "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
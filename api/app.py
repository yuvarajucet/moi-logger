from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

CORS(app, resources={r"/add": {"origins": "http://127.0.0.1:5500"}})
CORS(app)

def create_db_file():
     conn = sqlite3.connect('sqlite.db')
     cursor = conn.cursor()
     cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        s_no INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        area TEXT NOT NULL,
                        amount REAL NOT NULL
                    )''')
     conn.commit()
     conn.close()

# Function to create a connection to the SQLite database
def get_db_connection():
    create_db_file()
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint to handle the AJAX data and store it in the database
@app.route('/add', methods=['POST'])
def add_data():
    try:
        data = request.get_json()
        name = data.get('name')
        amt = data.get('amt')
        area = data.get('area')


        # Store the data in the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO data (name, area, amount) VALUES (?, ?, ?)",
                           (name, amt, area))
            conn.commit()

        return jsonify({"message": "Data added successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    app.run(debug=True)

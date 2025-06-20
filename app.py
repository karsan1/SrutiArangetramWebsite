from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize the database
conn = sqlite3.connect('rsvps.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rsvps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        guests INTEGER DEFAULT 0,
        attending TEXT NOT NULL,
        message TEXT,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()

@app.route('/rsvp', methods=['POST'])
def save_rsvp():
    data = request.get_json()
    try:
        conn = sqlite3.connect('rsvps.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rsvps (first_name, last_name, email, guests, attending, message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('firstName', '').strip(),
            data.get('lastName', '').strip(),
            data.get('email', '').strip(),
            int(data.get('guests', 0)),
            data.get('attending', '').strip(),
            data.get('message', '').strip()
        ))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

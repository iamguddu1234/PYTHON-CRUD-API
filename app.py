#from flask import Flask, jsonify, request
import mysql.connector
from flask import jsonify, request, Flask

app = Flask(__name__)

# MySQL connection details
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",  # Set your MySQL root password if any
    database="notes_app"
)

cursor = db.cursor()

# Create a new note
@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    title = data['title']
    content = data['content']

    query = "INSERT INTO notes (title, content) VALUES (%s, %s)"
    cursor.execute(query, (title, content))
    db.commit()

    return jsonify({'message': 'Note created successfully'}), 201

# Get all notes
@app.route('/notes', methods=['GET'])
def get_notes():
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    results = []
    for note in notes:
        results.append({'id': note[0], 'title': note[1], 'content': note[2]})

    return jsonify(results)

# Update a note
@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.json
    title = data['title']
    content = data['content']

    query = "UPDATE notes SET title = %s, content = %s WHERE id = %s"
    cursor.execute(query, (title, content, id))
    db.commit()

    return jsonify({'message': 'Note updated successfully'})

# Delete a note
@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    query = "DELETE FROM notes WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()

    return jsonify({'message': 'Note deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

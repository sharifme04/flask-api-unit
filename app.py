from flask import Flask, jsonify

app = Flask(__name__)

# Our list of books (stored in memory, no database yet)
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]


@app.route('/api/books', methods=['GET'])
def handle_books():
    return jsonify(books)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

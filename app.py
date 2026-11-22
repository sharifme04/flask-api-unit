from flask import Flask, jsonify, request

app = Flask(__name__)

# Our list of books (stored in memory, no database yet)
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]
# Add fake books so that there are 100 in total (used to test pagination)
books += [
    {"id": i, "title": f"Sample Book {i}", "author": f"Author {i % 5 + 1}"}
    for i in range(3, 101)
]


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


def validate_book_data(data):
    """A book must be a JSON object with a title and an author."""
    if not isinstance(data, dict) or "title" not in data or "author" not in data:
        return False
    return True


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        # Get the new book data from the client
        new_book = request.get_json(silent=True)
        if not validate_book_data(new_book):
            return jsonify({"error": "Invalid book data"}), 400

        # Generate a new ID for the book
        new_id = max((book['id'] for book in books), default=0) + 1
        new_book['id'] = new_id

        # Add the new book to our list
        books.append(new_book)

        # Return the new book data to the client
        return jsonify(new_book), 201
    else:
        # Optional filter: /api/books?author=George Orwell
        result = books
        author = request.args.get('author')
        if author:
            result = [book for book in books if book.get('author') == author]

        # Pagination: /api/books?page=2&limit=10
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
        except ValueError:
            return jsonify({"error": "page and limit must be integers"}), 400
        if page < 1 or limit < 1:
            return jsonify({"error": "page and limit must be positive"}), 400

        start_index = (page - 1) * limit
        end_index = start_index + limit

        response = jsonify(result[start_index:end_index])
        # Let clients know how many books exist in total
        response.headers['X-Total-Count'] = str(len(result))
        return response


def find_book_by_id(book_id):
    """Find the book with the id `book_id`.
    If there is no book with this id, return None."""
    for book in books:
        if book['id'] == book_id:
            return book
    return None


@app.route('/api/books/<int:id>', methods=['PUT'])
def handle_book(id):
    # Find the book with the given ID
    book = find_book_by_id(id)

    # If the book wasn't found, return a 404 error
    if book is None:
        return '', 404

    # Update the book with the new data
    new_data = request.get_json()
    book.update(new_data)

    # Return the updated book
    return jsonify(book)


@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = find_book_by_id(id)
    if book is None:
        return '', 404
    return jsonify(book)


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    # Find the book with the given ID
    book = find_book_by_id(id)

    # If the book wasn't found, return a 404 error
    if book is None:
        return '', 404

    # Remove the book from the list
    books.remove(book)

    # Return the deleted book
    return jsonify(book)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

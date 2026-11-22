# flask-api-unit

A small RESTful Flask API for managing books, built step by step while learning about APIs.

## Setup

```
pip install -r requirements.txt
python3 app.py
```

The server runs on `http://localhost:5000`.

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/books` | List books. Supports `?author=`, `?page=` and `?limit=` (default 10 per page). The `X-Total-Count` header holds the total number of books. Rate limited to 10 requests per minute. |
| GET | `/api/books/<id>` | Get one book |
| POST | `/api/books` | Create a book. JSON body needs `title` and `author` |
| PUT | `/api/books/<id>` | Update a book |
| DELETE | `/api/books/<id>` | Delete a book |

Errors are returned as JSON (`400`, `404`, `405`, `429`).

## Client script

`client.py` reads all the books, 10 at a time, until none are left:

```
python3 client.py [BASE_URL]
```

from flask import Flask, jsonify, abort, request, make_response
from flaskext.mysql import MySQL
.
.
app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'xxx'
app.config['MYSQL_DATABASE_USER'] = 'xxx'
app.config['MYSQL_DATABASE_PASSWORD'] = 'xxx'
app.config['MYSQL_DATABASE_DB'] = 'xxx'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

def init_bookstore_db():
    drop_table = 'DROP TABLE IF EXISTS bookstore_db.books;'
    books_table = """
    CREATE TABLE bookstore_db.books(
    book_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100),
    is_sold BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (book_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    data = """
    INSERT INTO bookstore_db.books (title, author, is_sold)
    VALUES
        ("Where the Crawdads Sing", "Delia Owens", 1 ),
        ("The Vanishing Half: A Novel", "Brit Bennett", 0),
        ("1st Case", "James Patterson, Chris Tebbetts", 0);
    """
    cursor.execute(drop_table)
    cursor.execute(books_table)
    cursor.execute(data)

def get_all_books():
    query = """
    SELECT * FROM books;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    books =[{'book_id':row[0], 'title':row[1], 'author':row[2], 'is_sold': bool(row[3])} for row in result]
    return books

def find_book(id):
    query = f"""
    SELECT * FROM books WHERE book_id={id};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    book = None
    if row is not None:
        book = {'book_id':row[0], 'title':row[1], 'author':row[2], 'is_sold': bool(row[3])}
    return book

def insert_book(title, author):
    insert = f"""
    INSERT INTO books (title, author)
    VALUES ('{title}', '{author}');
    """
    cursor.execute(insert)

    query = f"""
    SELECT * FROM books WHERE book_id={cursor.lastrowid};
    """
    cursor.execute(query)
    row = cursor.fetchone()

    return {'book_id':row[0], 'title':row[1], 'author':row[2], 'is_sold': bool(row[3])}

def change_book(book):
    update = f"""
    UPDATE books
    SET title='{book['title']}', author = '{book['author']}', is_sold = {book['is_sold']}
    WHERE book_id= {book['book_id']};
    """
    cursor.execute(update)

    query = f"""
    SELECT * FROM books WHERE book_id={book['book_id']};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return {'book_id':row[0], 'title':row[1], 'author':row[2], 'is_sold': bool(row[3])}

def remove_book(book):
    delete = f"""
    DELETE FROM books
    WHERE book_id= {book['book_id']};
    """
    cursor.execute(delete)

    query = f"""
    SELECT * FROM books WHERE book_id={book['book_id']};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return True if row is None else False

@app.route('/')
def home():
    return "Welcome to Turan's Bookstore API Service"

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books':get_all_books()})

@app.route('/books/<int:book_id>', methods = ['GET'])
def get_book(book_id):
    book = find_book(book_id)
    if book == None:
        abort(404)
    return jsonify({'book found': book})

@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    return jsonify({'newly added book':insert_book(request.json['title'], request.json.get('author', ''))}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = find_book(book_id)
    if book == None:
        abort(404)
    if not request.json:
        abort(400)
    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    book['is_sold'] = int(request.json.get('is_sold', int(book['is_sold'])))
    return jsonify({'updated book': change_book(book)})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = find_book(book_id)
    if book == None:
        abort(404)
    return jsonify({'result':remove_book(book)})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

if __name__== '__main__':
    init_bookstore_db()
    app.run(host='0.0.0.0', port=80)

from flask import Flask, render_template, request, redirect, url_for
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

initialize_cli = AppGroup('initialize')


@initialize_cli.command('database')
def initialize_database():
    with app.app_context():
        db.create_all()
    print('Database initialized.')


app.cli.add_command(initialize_cli)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)


@app.route('/book')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('edit_book.html', book=book)


@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

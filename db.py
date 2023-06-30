from app import db
from models import Book

db.create_all()

book1 = Book(title='The Great Gatsby', author='F. Scott Fitzgerald', year=1925)
book2 = Book(title='To Kill a Mockingbird', author='Harper Lee', year=1960)

db.session.add(book1)
db.session.add(book2)
db.session.commit()

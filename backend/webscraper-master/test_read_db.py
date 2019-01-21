import ZODB, ZODB.FileStorage
import os

path = 'C:\\Users\\blins\\Documents\\Projects\\Ultimate Shopping Website\\scraper\\test_book_db'
storage = ZODB.FileStorage.FileStorage(os.path.join(path, 'barnesnoble.fs'))
db = ZODB.DB(storage)
conn = db.open()

root = conn.root()

for k in root.books.keys():
    print(root.books[k].title + " " + root.books[k].author)
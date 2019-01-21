import ZODB, ZODB.FileStorage
import BTrees, BTrees.OOBTree
import os
import transaction

class BookDatabase:
    """
    Interface for interacting with database of books
    """

    def __init__(self, path):
        storage = ZODB.FileStorage.FileStorage(path)
        db = ZODB.DB(storage)
        conn = db.open()
        self.root = conn.root()

    def create_database(self):
        self.root.books = BTrees.OOBTree.BTree()
        transaction.commit()

    def add_listing(self, book, listing):
        if book.name not in self.root.books.keys():
            book.add_listing(listing)
            self.root.books.update( [ (book.name, book) ] )
        else:
            self.root.books[book.name].add_listing(listing)
        transaction.commit()

if __name__ == '__main__':
    path = 'C:\\Users\\blins\\Documents\\Projects\\Ultimate Shopping Website\\scraper\\test_book_db'
    db = BookDatabase()
    #db.create_database()
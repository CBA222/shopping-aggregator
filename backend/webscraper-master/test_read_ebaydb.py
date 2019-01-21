import ZODB, ZODB.FileStorage

path = '/Users/apple/Desktop/Projects/ebaydb/ebaydb.fs'

storage = ZODB.FileStorage.FileStorage(path)
db = ZODB.DB(storage)
conn = db.open()
root = conn.root()


for i, k in enumerate(root.products.values()):
    print(i, k.image)
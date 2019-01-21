from sql_database.db_interface import DatabaseInterface
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:lego_10010@localhost/product_database_2')
conn = engine.connect()
db = DatabaseInterface(conn)
db.add_listing('Sony IMAX Camera',['image1.png'], 'thumb.png', 'description','877653006556','dhkas','Wal-Mart','1599.99','walmart.com')
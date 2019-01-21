from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.dialects import postgresql

engine = create_engine('postgresql://postgres:lego_10010@localhost/product_database_2')

metadata = MetaData()

products = Table('products', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('image_urls', postgresql.ARRAY(String, dimensions=1)),
    Column('thumbnail', String),
    Column('description', String),
    Column('upc', String, unique=True),
    Column('model_number', String, unique=True),
    Column('listings', JSON)
)

metadata.create_all(engine)

metadata2 = MetaData()
db_store_info = Table('db_store_info', metadata2,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('stored_products', postgresql.ARRAY(String, dimensions=1))
)
from multiprocessing import Process, Pool, Manager
from readers.storereader import StoreReader

from sqlalchemy import create_engine

class CustomObject:

    def __init__(self, hello):
        self.hello = hello

class DBInterface:

    def __init__(self, path):
        engine = create_engine(path)
        self.conn = engine.connect()

    def do_something(self):
        pass


class Runner:

    def __init__(self, objs, engine):
        self.objs = objs
        m = Manager()
        self.l = m.list()
        self.engine = engine

    def foo(self, obj):
        conn = self.engine.connect()

    def run(self):
        pool = Pool(4)
        pool.map(self.foo, self.objs)
        pool.close()
        pool.join()

if __name__ == '__main__':
    objs = [StoreReader(), StoreReader()]
    path = 'postgresql://postgres:lego_10010@localhost/product_database_2'
    runner = Runner(objs, create_engine(path))
    runner.run()
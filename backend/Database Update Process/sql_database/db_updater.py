from multiprocessing import Manager, Pool
from sqlalchemy import create_engine
import time, copy, pickle

from .db_interface import DatabaseInterface

def force_two_digits(self, x):
    if x < 10:
        return '0' + str(x)

class DatabaseUpdater:
    """
    This class is responsible for taking data collected by StoreReader objects
    and putting it into the database in a proper manner
    """
    
    def __init__(self, db_path, readers, thread_count=5):
        self.db_path = db_path
        self.readers = readers

        self.thread_count = thread_count
        self.test_mode = False

        self.logs = []
        self.id = 0

        self.reader_ids = {}

        i = 1
        for r in self.readers:
            self.reader_ids[i] = r.vendor
            r.set_id(i)
            r.set_logger(self)
            i += 1

    def set_manager_dict(self, d):
        self.manager_dict = d
        self.manager_dict[self.id] = []

    def read_update(self, reader):
        """
        Helper function: Reads in a single store's inventory and updates the database
        """
        engine = create_engine(self.db_path)
        conn = engine.connect()
        db_interface = DatabaseInterface(conn)
        
        if self.test_mode==False:
            data = reader.read_all()
        else:
            data = reader.read_test()

        for listing in data:
            db_interface.add_listing(
                product_name=listing[0]['name'],
                product_image_urls=listing[0]['image_urls'],
                product_thumbnail=listing[0]['thumbnail'],
                product_description=listing[0]['description'],
                product_upc=listing[0]['upc'],
                product_model_number=listing[0]['model_number'],

                listing_vendor=listing[1]['vendor'],
                listing_price=listing[1]['price'],
                listing_url=listing[1]['url']
            )

        self.log(self.id, 'Successfuly updated database with data from {}'.format(reader.vendor))

    def update_all(self, test=False):
        """
        Gather data from each reader and put into database
        """
        self.log(self.id, "Beginning database update process")

        self.test_mode = test

        pool = Pool(self.thread_count)
        pool.map(self.read_update, self.readers)
        pool.close()
        pool.join()

        self.log(self.id, "End of database update process")

    def log(self, id, msg):
        """
        Logging function
        Each store stores their logs through this function
        """
        current_time = time.localtime(time.time())
        current_time_string = "{}:{}:{}".format(current_time.tm_hour, current_time.tm_min, current_time.tm_sec)

        msg = "{} | {}".format(current_time_string, msg)
        self.logs.append(msg)

        l = self.manager_dict[id]
        l.append(msg)
        self.manager_dict[id] = l

        print(msg)

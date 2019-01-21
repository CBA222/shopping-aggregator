import abc

class StoreReader(object):

    def __init__(self):
        pass

    def set_id(self, id):
        self.id = id

    def set_logger(self, logger):
        self.logger = logger

    def log(self, msg):
        self.logger.log(self.id, msg)

    @abc.abstractmethod
    def read_all(self):
        pass

    @abc.abstractmethod
    def read_test(self):
        pass
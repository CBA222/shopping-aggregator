from http.server import HTTPServer
from admin_panel.request_handler import MainRequestHandler
from sql_database.db_updater import DatabaseUpdater
from sql_database.db_interface import DatabaseInterface

from multiprocessing import Process, Manager
import signal, sys

def exit_handler(sig, frame):
    print('Quitting Update Server')
    sys.exit(0)

class CustomServer(HTTPServer):
    def serve_forever(self, manager_dict, store_ids):
        self.RequestHandlerClass.set_manager_dict(self.RequestHandlerClass, manager_dict)
        self.RequestHandlerClass.set_store_ids(self.RequestHandlerClass, store_ids)
        HTTPServer.serve_forever(self)

class UpdateServer:

    def __init__(self, db_path, server_address, readers):
        self.admin_panel_server = CustomServer(server_address, MainRequestHandler)

        self.my_readers = readers
        self.db_updater = DatabaseUpdater(db_path, self.my_readers)
        
    def start(self, test=False):
        signal.signal(signal.SIGINT, exit_handler)
        print("Initializing Update Server, press CTRL-C to exit")

        manager = Manager()
        self.logs_dict = manager.dict()

        for r in self.my_readers:
            self.logs_dict[r.id] = []

        self.db_updater.set_manager_dict(self.logs_dict)

        self.server_process = Process(target=self.admin_panel_server.serve_forever, args=(self.logs_dict, self.db_updater.reader_ids, ))
        self.update_process = Process(target=self.db_updater.update_all, args=(test,)) 

        self.server_process.start()
        self.update_process.start()
        self.server_process.join()
        self.update_process.join()
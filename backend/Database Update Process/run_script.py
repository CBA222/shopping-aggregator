"""
This script loads configuration data and starts the update server
"""
from update_server import UpdateServer
import config

readers = [r['class'](**r['attrs']) for r in config.READERS_TO_USE if r['use'] == True]

server_address = (config.ADMIN_PANEL['address'], config.ADMIN_PANEL['port'])
db_path = config.DATABASE['path']

server = UpdateServer(db_path, server_address, readers)
server.start(test=config.TEST)
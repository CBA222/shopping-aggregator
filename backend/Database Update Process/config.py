"""
Configuration file for database update server
"""
import readers_definitions

TEST = False

ADMIN_PANEL = {
    "address": "127.0.0.1",
    "port": 8081
}

DATABASE = {
    "path": "postgresql://postgres:lego_10010@localhost/product_database_2"
}

READERS_TO_USE = [
    {
        "use": True,
        "class": readers_definitions.READERS["bestbuy"],
        "attrs": {
            "apikey": "Xsk22axb3WQ4bA3KCUbuA3Qf",
            "page_limit": 3,
            "categories_to_skip": ["abcat0600000"]
        }
    },
    {
        "use": False,
        "class": readers_definitions.READERS["walmart"],
        "attrs": {
            "apikey": "rj9w6a59zbyckgdn4e7e9rqz",
            "page_limit": 3
        }
    }
]


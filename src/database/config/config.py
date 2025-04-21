import os
from dotenv import load_dotenv


# Connect to database
def load_config():
    """ Connect to the PostgreSQL database server """
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    config = {}
    config["host"] = DB_HOST
    config["database"] = DB_NAME
    config["user"] = DB_USER
    config["password"] = DB_PASSWORD
    return config


if __name__ == '__main__':
    load_config()

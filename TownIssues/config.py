import os

class Config:
    SECRET_KEY = os.urandom(12).hex()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CONN_STR')

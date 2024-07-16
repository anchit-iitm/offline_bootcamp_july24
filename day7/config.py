
class config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None

class localDev(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test2.sqlite3"
    SECRET_KEY = "shhh.... its very ssecret"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TRACKABLE = True

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_DEFAULT_TIMEOUT = 15

    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'admin@gmail.in'

class production(config):
    SQLALCHEMY_DATABASE_URI = None
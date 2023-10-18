

APP_HOST = '127.0.0.1'
APP_PORT = 8000

DB_NAME = 'CRUD'
DB_USER = 'root'
DB_HOST = 'db'
DB_PORT = '5432'
DB_PASSWORD = 'root'


TEST_DB_NAME = DB_NAME + "_test"

SECRET = "SECRET"

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print(DB_URL)
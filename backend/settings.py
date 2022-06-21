import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME  = os.getenv('DB_NAME')
DB_TEST = os.getenv('DB_TEST')

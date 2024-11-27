from os import environ

from dotenv import load_dotenv

load_dotenv()

DATA_PATH = environ.get('DATA_PATH')

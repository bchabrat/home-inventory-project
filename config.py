import os
DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
CORS_HEADERS = 'Content-Type'
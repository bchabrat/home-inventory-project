import os
DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SECRET_KEY = os.environ['SECRET_KEY']
SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
CORS_HEADERS = 'Content-Type'
SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
USER_APP_NAME = "Flask-User QuickStart App"  # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False  # Disable email authentication
USER_ENABLE_USERNAME = True  # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = False  # Simplify register form


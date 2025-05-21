import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'HelpDeskApp12345')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///helpdeskticketingsystem.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '40e35e41fcc9f0b1b7bd39bcfdcfe7fd37b544ef3f8ced4cd85b925736258170')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///helpdeskticketingsystem.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

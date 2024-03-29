import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config (object) :

    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL') 
        # 'sqlite:///' + os.path.join(basedir, 'application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'come-on-guess' 

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['techgirl0076@gmail.com']
    LANGUAGES =['en', 'es', 'it']

    POSTS_PER_PAGE = 25



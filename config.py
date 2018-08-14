#SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:apple@localhost:3306/microblog"
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#CSRF_ENABLED = True
#SECRET_KEY = 'you-will-never-guess'
#POSTS_PER_PAGE = 1
#WHOOSH_BASE='path/to/whoosh/base'

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:apple@localhost:3306/microblog"
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 1
    CSRF_ENABLED = True
    #WHOOSH_BASE = os.path.join(basedir, 'search.db')
    #WHOOSH_BASE = os.path.join(basedir, 'search.db')
    DEBUG = True

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    # administrator list
    ADMINS = ['2465272199@qq.com']

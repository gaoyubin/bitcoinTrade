from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
app=Flask(__name__)
app.config.from_object(Config)
'''
db=SQLAlchemy(app)
bootstrap=Bootstrap(app)

loginmanager=LoginManager()
loginmanager.session_protection='strong'
loginmanager.login_view='login'
loginmanager.init_app(app)


'''


from app import views

if not app.debug:
    print "app.debug",app.debug
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
        credentials = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
    mail_handler = SMTPHandler((app.config["MAIL_SERVER"], app.config["MAIL_PORT"]), 'no-reply@' + app.config["MAIL_SERVER"], app.config["ADMINS"], 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


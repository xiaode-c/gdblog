# coding:utf-8

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown

from config import config


db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'admin.login'
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    from .admin import admin as admin_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)

    #添加路由和自定义的错误页面
    return app

from flask import Flask
from flask_login import LoginManager

from api import jobs_api, user_api
from data import global_init

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key_secret_a_lot'

login_manager = LoginManager()
login_manager.init_app(app)

global_init("db/mars.db")

from . import view

app.register_blueprint(jobs_api.blueprint)
app.register_blueprint(user_api.blueprint)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

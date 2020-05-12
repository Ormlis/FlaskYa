from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from api.resources import users_resource
from data import global_init

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key_secret_a_lot'

api = Api(app)

api.add_resource(users_resource.UserListResource, '/api/v2/users')
api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')

login_manager = LoginManager()
login_manager.init_app(app)

global_init("db/mars.db")

from . import view

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

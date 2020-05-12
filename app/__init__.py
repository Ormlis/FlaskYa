from flask import Flask
from data import global_init

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key_secret_a_lot'

global_init("db/mars.db")

from . import view

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

import datetime

from flask import Flask, render_template
from app import app
from data import *


@app.route('/')
@app.route('/index')
def index():
    session = create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', actions=jobs)

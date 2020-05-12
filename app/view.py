from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user

from app import app, login_manager
from app.forms import *
from data import *


@app.route('/')
@app.route('/index')
def index():
    session = create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', actions=jobs, title='Works log')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/job/new', methods=['GET', 'POST'])
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.id == form.team_leader.data).first()
        if not user:
            return render_template('job_edit.html', title='Adding a job', title_form='Adding a job',
                                   form=form, message='Wrong team leader id')
        job = Jobs(
            job=form.job.data,
            collaborators=form.collaborators.data,
            work_size=form.work_size.data,
            is_finished=form.is_finished.data,
            team_leader=form.team_leader.data
        )
        user.jobs.append(job)
        session.commit()
        return redirect('/')
    return render_template('job_edit.html', title='Adding a job', title_form='Adding a job',
                           form=form)

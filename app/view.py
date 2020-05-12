from flask import render_template, redirect, request, abort, make_response, jsonify
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
@login_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.id == form.team_leader.data).first()
        if not user:
            return render_template('job_edit.html', title='Adding a job', title_form='Adding a job',
                                   form=form, message='Wrong team leader id')

        category = session.query(Category).filter(Category.id == form.category.data).first()
        if not category:
            category = Category(id=form.category.data)
            session.add(category)
        job = Jobs(
            job=form.job.data,
            collaborators=form.collaborators.data,
            work_size=form.work_size.data,
            is_finished=form.is_finished.data,
            team_leader=form.team_leader.data
        )
        job.categories.append(category)
        user.jobs.append(job)
        session.commit()
        return redirect('/')
    return render_template('job_edit.html', title='Adding a job', title_form='Adding a job',
                           form=form)


@app.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = JobForm()
    session = create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        abort(404)
    if job.team_leader != current_user.id and current_user.id != 1:
        abort(403)
    if request.method == 'GET':
        form.job.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.is_finished.data = job.is_finished
        form.collaborators.data = job.collaborators
        form.category.data = job.categories[0].id
    if form.validate_on_submit():
        job.categories.remove(job.categories[0])
        category = session.query(Category).filter(Category.id == form.category.data).first()
        if not category:
            category = Category(id=form.category.data)
            session.add(category)
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.is_finished = form.is_finished.data
        job.collaborators = form.collaborators.data
        job.work_size = form.work_size.data
        job.categories.append(category)
        session.merge(job)
        session.commit()
        return redirect('/')
    return render_template('job_edit.html', title='Job editing', form=form,
                           title_form='Job editing')


@app.route('/job/<int:job_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    session = create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        abort(404)
    if job.team_leader != current_user.id and current_user.id != 1:
        abort(403)
    session.delete(job)
    session.commit()
    return redirect('/')


@app.route('/departments')
def departments_page():
    session = create_session()
    departments = session.query(Departments).all()
    return render_template('departments.html', departments=departments, title='List of departments')


@app.route('/department/new', methods=['GET', 'POST'])
@login_required
def new_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = create_session()
        department = Departments(
            title=form.title.data,
            members=form.members.data,
            chief=current_user.id,
            email=form.email.data,
        )
        current_user.departments.append(department)
        session.merge(current_user)
        session.commit()
        return redirect('/departments')
    return render_template('department_edit.html', title='Adding a department',
                           title_form='Adding a department',
                           form=form)


@app.route('/department/<int:department_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    session = create_session()
    department = session.query(Departments).filter(Departments.id == department_id).first()
    if not department:
        abort(404)
    if department.chief != current_user.id and current_user.id != 1:
        abort(403)
    if request.method == 'GET':
        form.title.data = department.title
        form.members.data = department.members
        form.email.data = department.email
    if form.validate_on_submit():
        department.title = form.title.data
        department.members = form.members.data
        department.email = form.email.data
        session.merge(department)
        session.commit()
        return redirect('/departments')
    return render_template('department_edit.html', title='Department editing', form=form,
                           title_form='Department editing')


@app.route('/department/<int:department_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_department(department_id):
    session = create_session()
    department = session.query(Departments).filter(Departments.id == department_id).first()
    if not department:
        abort(404)
    if department.chief != current_user.id and current_user.id != 1:
        abort(403)
    session.delete(department)
    session.commit()
    return redirect('/departments')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

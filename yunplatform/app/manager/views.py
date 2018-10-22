from . import manager
from flask import abort, render_template, redirect, request, url_for, flash, current_app
from app.models import User, Role, Device,Alert
from app import db
from flask_login import current_user, login_required, login_user, logout_user
from .forms import EditUserForm, AddUserFrom, SearchForm
from app.decorators import decorator_permission, decorator_admin


@manager.route('/manager_all_devices')
@decorator_admin
def manager_all_devices():
    #devices = Device.query.all()
    page = request.args.get('page', type=int, default=1)
    devices = Device.query.paginate(page=page, per_page=5, error_out=False)
    return render_template('manager/all_devices.html', devices=devices)


@manager.route('/manager_all_users', methods=['GET', 'POST'])
@decorator_admin
def manager_all_users():
    form = SearchForm()
    print('2')
    if form.validate_on_submit():
        print('3')
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        print(user)
        return redirect(url_for('main.user_info', id=user.id))
    page = request.args.get('page', type=int, default=1)
    users = User.query.paginate(page=page, per_page=5, error_out=False)
    return render_template('manager/glzx.html', users=users, form=form)


@manager.route('/manager_edit_user', methods=['GET', 'POST'])
@decorator_admin
def manager_edit_user():
    id = request.args.get('id')
    if id is None:
        abort(404)
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    form = EditUserForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.confirmed = form.confirmed.data
        user.location = form.location.data
        user.role_id = form.role_id.data
        user.about_me = form.about_me.data
        if len(form.password.data) != 0 :
            user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('manager.manager_all_users', id=user.id))
    form.name.data = user.name
    form.email.data = user.email
    form.location.data = user.location
    form.role_id.data = user.role_id
    form.about_me.data = user.about_me
    form.confirmed.data = user.confirmed
    return render_template('manager/edit_user.html', form=form)


@manager.route('/add_user', methods=['GET', 'POST'])
@decorator_admin
def add_user():
    form = AddUserFrom()
    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.confirmed = form.confirmed.data
        user.location = form.location.data
        user.role_id = form.role_id.data
        user.about_me = form.about_me.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        # user.API_KEY = user.generate_confirmed_token()
        return redirect(url_for('manager.manager_all_users'))
    return render_template('manager/add_user.html', form=form)


@manager.route('/delete_user')
@decorator_admin
def delete_user():
    uid = request.args.get('uid')
    if uid is None:
        abort(404)
    user = User.query.filter_by(id=uid).first()
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manager.manager_all_users'))


@manager.route('/delete_alert')
@decorator_admin
def delete_alert():
    aid = request.args.get('aid')
    if aid is None:
        abort(404)
    alert = Alert.query.filter_by(id=aid).first()
    if alert is None:
        abort(404)
    db.session.delete(alert)
    db.session.commit()
    return redirect(url_for('main.alert'))






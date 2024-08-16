from flask                           import Blueprint, request, render_template, redirect, url_for
from flask_login                     import logout_user

Auth = Blueprint('auth', __name__, url_prefix='/auth')

@Auth.route('/')
def Index():
    return redirect(url_for('Auth.Login'))

@Auth.route('/login' , methods=['GET','POST'])
def Login():
    if request.method == 'GET'  : return render_template('Auth/Login.html')
    if request.method == 'POST' :
        raise NotImplementedError('Route not implemented yet')

@Auth.route('/logout' , methods=['GET','POST'])
def Logout():
    logout_user()
    return redirect(url_for('Root.Index'))

@Auth.route('/register' , methods=['GET','POST'])
def Register():
    if   request.method == 'GET'  : return render_template('Auth/Register.html')
    elif request.method == 'POST' :
        raise NotImplementedError('Route not implemented yet')
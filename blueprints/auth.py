from flask                           import Blueprint, request, render_template, redirect, url_for
from flask_login                     import logout_user

Auth = Blueprint('auth', __name__, url_prefix='/auth')

@Auth.route('/')
def index():
    return redirect(url_for('auth.login'))

@Auth.route('/login' , methods=['GET','POST'])
def login():
    if request.method == 'GET' : return render_template('auth/login.html')
    if request.method == 'POST':
        raise NotImplementedError('Route not implemented yet')

@Auth.route('/logout' , methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('root.index'))

@Auth.route('/register' , methods=['GET','POST'])
def register():
    if   request.method == 'GET'  : return render_template('auth/register.html')
    elif request.method == 'POST' :
        raise NotImplementedError('Route not implemented yet')
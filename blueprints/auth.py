from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import logout_user

from classes.component.sqlmanager import SQLManager

def Auth(SQLManager:SQLManager) -> Blueprint:

    bp = Blueprint('auth', __name__, url_prefix='/auth')

    @bp.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @bp.route('/login' , methods=['GET','POST'])
    def login():
        if request.method == 'GET' : return render_template('auth/login.html')
        if request.method == 'POST':
            raise NotImplementedError('Route not implemented yet')

    @bp.route('/logout' , methods=['GET','POST'])
    def logout():
        logout_user()
        return redirect(url_for('root.index'))

    @bp.route('/register' , methods=['GET','POST'])
    def register():
        if   request.method == 'GET'  : return render_template('auth/register.html')
        elif request.method == 'POST' :
            raise NotImplementedError('Route not implemented yet')
    
    return bp
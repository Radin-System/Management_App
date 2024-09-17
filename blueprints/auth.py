from flask import Blueprint, abort, request, render_template, redirect, url_for
from flask_login import logout_user, login_user

from classes.component import ComponentContainer, SQLManager
from classes.policy.input import PasswordPolicy, UsernamePolicy
from classes.tool import ToolContainer

def Auth(CC:ComponentContainer, TC:ToolContainer) -> Blueprint:
    SQL:SQLManager = CC.Get('Main_SQLManager')

    bp = Blueprint('auth', __name__, url_prefix='/auth')

    @bp.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @bp.route('/login' , methods=['GET','POST'])
    def login():
        if request.method == 'GET' : return render_template('auth/login.html')
        if request.method == 'POST':
            # Getting requierd form fields
            Loging_User = request.form.get('username')
            Loging_Pass = request.form.get('password')
            
            # Check for Input policy
            try: 
                Loging_User = UsernamePolicy.Apply(Loging_User)
                Loging_Pass = PasswordPolicy.Apply(Loging_Pass)
            except: 
                return abort(401)

            # Check if filds are proprly inputed
            if Loging_User and Loging_Pass:
                # getting the user
                User = SQL.Query(SQL.User,First=True, username=Loging_User)
                if User:
                    # Comparing password
                    if User.password == Loging_Pass :
                        login_user(User)
                        return redirect(url_for('root.index'))

            return abort(401)

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
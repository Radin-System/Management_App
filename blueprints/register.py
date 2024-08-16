from flask import Blueprint, render_template
from flask_login import current_user
from classes.pagesettings import PageSetting

Register = Blueprint('register', __name__, url_prefix='/register')

@Register.context_processor
def Context_Processor() -> dict:
    return dict(Current_User=current_user, PageSetting=PageSetting())

@Register.route('/')
def index():
    return render_template('register/index.html')

@Register.route('/form')
def form():
    return render_template('register/form.html')
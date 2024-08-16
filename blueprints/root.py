from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from classes.pagesettings import PageSetting

Root = Blueprint('root', __name__, url_prefix='/')

@Root.context_processor
def Context_Processor() -> dict:
    return dict(Current_User=current_user, PageSetting=PageSetting())

@Root.route('/')
def index():
    return render_template('index.html')

@Root.route('/home')
def Home():
    return render_template('Home.html')

@Root.route('/services')
def Services():
    return render_template('Services.html')

@Root.route('/about')
def About():
    return render_template('About.html')

@Root.route('/under-construction')
def under_construction():
    return render_template('under-construction.html')

@Root.route('/favicon.ico')
def Favicon():
    return redirect(url_for('static',filename='favicon.ico'))

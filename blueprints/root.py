from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from classes.component.sqlmanager import SQLManager
from classes.pagesettings import PageSetting

def Root(SQLManager:SQLManager) -> Blueprint:

    bp = Blueprint('root', __name__, url_prefix='/')

    @bp.context_processor
    def Context_Processor() -> dict:
        return dict(Current_User=current_user, PageSetting=PageSetting())

    @bp.route('/')
    def index():
        return render_template('index.html')

    @bp.route('/home')
    def Home():
        return render_template('Home.html')

    @bp.route('/services')
    def Services():
        return render_template('Services.html')

    @bp.route('/about')
    def About():
        return render_template('About.html')

    @bp.route('/under-construction')
    def under_construction():
        return render_template('under-construction.html')

    @bp.route('/favicon.ico')
    def Favicon():
        return redirect(url_for('static',filename='favicon.ico'))

    return bp
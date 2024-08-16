from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from classes.component.sqlmanager import SQLManager

def Root(SQL:SQLManager) -> Blueprint:

    bp = Blueprint('root', __name__, url_prefix='/')

    @bp.route('/')
    def index():
        return render_template('index.html')

    @bp.route('/home')
    def home():
        return render_template('Home.html')

    @bp.route('/under-construction')
    def under_construction():
        return render_template('under-construction.html')

    @bp.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static',filename='favicon.ico'))

    return bp
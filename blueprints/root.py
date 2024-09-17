from flask import Blueprint, redirect, render_template, url_for
from classes.component import ComponentContainer
from classes.tool import ToolContainer

def Root(CC:ComponentContainer, TC:ToolContainer) -> Blueprint:

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
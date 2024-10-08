from flask import Blueprint, redirect, render_template, url_for
from classes.component import ComponentContainer
from classes.tool import ToolContainer

def User(CC:ComponentContainer, TC:ToolContainer) -> Blueprint:

    bp = Blueprint('user', __name__, url_prefix='/user')

    @bp.route('/')
    def index():
        return redirect(url_for('user.profile'))

    @bp.route('/profile')
    def profile():
        return render_template('user/profile.html')

    return bp
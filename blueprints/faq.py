from flask import Blueprint, render_template
from flask_login import current_user
from classes.component.sqlmanager import SQLManager

def Faq(SQLManager:SQLManager) -> Blueprint:
        
    bp = Blueprint('faq', __name__, url_prefix='/faq')

    @bp.route('/')
    def index():
        return render_template('faq/index.html')

    return bp
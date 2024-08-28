from flask import Blueprint, render_template
from classes.component import ComponentContainer

def Faq(CC:ComponentContainer) -> Blueprint:
        
    bp = Blueprint('faq', __name__, url_prefix='/faq')

    @bp.route('/')
    def index():
        return render_template('faq/index.html')

    return bp
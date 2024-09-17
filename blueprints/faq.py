from flask import Blueprint, render_template
from classes.component import ComponentContainer
from classes.tool._container import ToolContainer

def Faq(CC:ComponentContainer, TC:ToolContainer) -> Blueprint:
        
    bp = Blueprint('faq', __name__, url_prefix='/faq')

    @bp.route('/')
    def index():
        return render_template('faq/index.html')

    return bp
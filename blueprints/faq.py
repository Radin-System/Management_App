from flask import Blueprint, render_template
from flask_login import current_user
from classes.component.sqlmanager import SQLManager
from classes.pagesettings import PageSetting

def Faq(SQLManager:SQLManager) -> Blueprint:
        
    bp = Blueprint('faq', __name__, url_prefix='/faq')

    @bp.context_processor
    def Context_Processor() -> dict:
        return dict(Current_User=current_user, PageSetting=PageSetting())

    @bp.route('/')
    def index():
        return render_template('faq/index.html')

    return bp
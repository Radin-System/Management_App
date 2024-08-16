from flask import Blueprint, render_template
from flask_login import current_user
from constants import PageSetting

Faq = Blueprint('faq', __name__, url_prefix='/faq')

@Faq.context_processor
def Context_Processor() -> dict:
    return dict(Current_User=current_user, PageSetting=PageSetting())

@Faq.route('/')
def index():
    return render_template('faq/index.html')

from flask import Blueprint, jsonify

from classes.component import ComponentContainer, SQLManager
from classes.tool import ToolContainer
from functions.web import Create_API_Response

def Api(CC:ComponentContainer, TC:ToolContainer) -> Blueprint:
    SQL:SQLManager = CC.Get('Main_SQLManager')

    bp = Blueprint('api', __name__, url_prefix='/endpoint/api')

    @bp.route('/')
    def index():
        Data = 'hi, welcome to simple client api'

        return jsonify(Create_API_Response(Data))

    @bp.route('/all-tokens',methods=['POST'])
    def all_tokens():
        raise NotImplementedError('route not implemented yet')

    @bp.route('/flush-tokens',methods=['POST'])
    def flush_tokens():
        raise NotImplementedError('route not implemented yet')

    @bp.route('/register-vnc')
    def register_vnc():
        raise NotImplementedError('route not implemented yet')

    return bp
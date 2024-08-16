from flask import Blueprint, jsonify
from functions.web import Create_Response

Api = Blueprint('api', __name__, url_prefix='/endpoint/api')

@Api.route('/')
def index():
    Data = 'hi, welcome to simple client api'

    return jsonify(Create_Response(Data))

@Api.route('/generate-token',methods=['POST'])
def generate_token():
    raise NotImplementedError('route not implemented yet')

@Api.route('/all-tokens',methods=['POST'])
def all_tokens():
    raise NotImplementedError('route not implemented yet')

@Api.route('/flush-tokens',methods=['POST'])
def flush_tokens():
    raise NotImplementedError('route not implemented yet')

@Api.route('/register-vnc')
def register_vnc():
    raise NotImplementedError('route not implemented yet')
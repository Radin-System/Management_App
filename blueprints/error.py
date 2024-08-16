from flask import Blueprint
from functions import Handle_Http_Error

Error = Blueprint('error', __name__)

@Error.app_errorhandler(400)
def bad_request_error(error):
    return Handle_Http_Error(error, 400)

@Error.app_errorhandler(401)
def unauthorized_error(error):
    return Handle_Http_Error(error, 401)

@Error.app_errorhandler(403)
def forbidden_error(error):
    return Handle_Http_Error(error, 403)

@Error.app_errorhandler(404)
def not_found_error(error):
    return Handle_Http_Error(error, 404)

@Error.app_errorhandler(405)
def method_not_allowed_error(error):
    return Handle_Http_Error(error, 405)

@Error.app_errorhandler(408)
def request_timeout_error(error):
    return Handle_Http_Error(error, 408)

@Error.app_errorhandler(409)
def conflict_error(error):
    return Handle_Http_Error(error, 409)

@Error.app_errorhandler(410)
def gone_error(error):
    return Handle_Http_Error(error, 410)

@Error.app_errorhandler(413)
def payload_too_large_error(error):
    return Handle_Http_Error(error, 413)

@Error.app_errorhandler(415)
def unsupported_media_type_error(error):
    return Handle_Http_Error(error, 415)

@Error.app_errorhandler(429)
def too_many_requests_error(error):
    return Handle_Http_Error(error, 429)

@Error.app_errorhandler(500)
def internal_server_error(error):
    return Handle_Http_Error(error, 500)

@Error.app_errorhandler(501)
def not_implemented_error(error):
    return Handle_Http_Error(error, 501)

@Error.app_errorhandler(502)
def bad_gateway_error(error):
    return Handle_Http_Error(error, 502)

@Error.app_errorhandler(503)
def service_unavailable_error(error):
    return Handle_Http_Error(error, 503)

@Error.app_errorhandler(504)
def gateway_timeout_error(error):
    return Handle_Http_Error(error, 504)

# To catch other unhandled errors, a catch-all handler can be added:
@Error.app_errorhandler(Exception)
def unhandled_exception_error(error):
    return Handle_Http_Error(error, 500, Description="An unexpected error occurred.")

from flask import Blueprint, Response, request, render_template
from classes.component import ComponentContainer
from functions.web import Create_API_Response
from functions.errorhandler import Handle_Error
from functions.callcenter import Create_Cisco_Error

def Error(CC:ComponentContainer) -> Blueprint:

    bp = Blueprint('error', __name__)

    def Base_HTTP_Error_Handling(error, status_code):
        # Create detailed error information for the template
        Error_Detail = Handle_Error(error, Code=status_code, Description=str(error), url=request.url, form=dict(request.form))

        #Error_Detail['traceback'] = 'NotImplemented' # waiting for Permission implementation
        #Error_Detail['url'] = 'NotImplemented' # waiting for Permission implementation
        #Error_Detail['form'] = 'NotImplemented' # waiting for Permission implementation

        # Handle the error based on the request path
        if request.path.startswith('/endpoint/api'):
            API_Response = Create_API_Response(Message=Error_Detail, Status='Error', Code=status_code)
            return Response(API_Response, mimetype='json/application'), status_code

        if request.path.startswith('/callcenter'):
            Xml = Create_Cisco_Error(Error_Detail=Error_Detail)
            return Response(Xml, mimetype='text/xml'), status_code

        else:
            return render_template('error.html', Error_Detail=Error_Detail), status_code

    @bp.app_errorhandler(400)
    def bad_request_error(error):
        return Base_HTTP_Error_Handling(error, 400)

    @bp.app_errorhandler(401)
    def unauthorized_error(error):
        return Base_HTTP_Error_Handling(error, 401)

    @bp.app_errorhandler(403)
    def forbidden_error(error):
        return Base_HTTP_Error_Handling(error, 403)

    @bp.app_errorhandler(404)
    def not_found_error(error):
        return Base_HTTP_Error_Handling(error, 404)

    @bp.app_errorhandler(405)
    def method_not_allowed_error(error):
        return Base_HTTP_Error_Handling(error, 405)

    @bp.app_errorhandler(408)
    def request_timeout_error(error):
        return Base_HTTP_Error_Handling(error, 408)

    @bp.app_errorhandler(409)
    def conflict_error(error):
        return Base_HTTP_Error_Handling(error, 409)

    @bp.app_errorhandler(410)
    def gone_error(error):
        return Base_HTTP_Error_Handling(error, 410)

    @bp.app_errorhandler(413)
    def payload_too_large_error(error):
        return Base_HTTP_Error_Handling(error, 413)

    @bp.app_errorhandler(415)
    def unsupported_media_type_error(error):
        return Base_HTTP_Error_Handling(error, 415)

    @bp.app_errorhandler(429)
    def too_many_requests_error(error):
        return Base_HTTP_Error_Handling(error, 429)

    @bp.app_errorhandler(500)
    def internal_server_error(error):
        return Base_HTTP_Error_Handling(error, 500)

    @bp.app_errorhandler(501)
    def not_implemented_error(error):
        return Base_HTTP_Error_Handling(error, 501)

    @bp.app_errorhandler(502)
    def bad_gateway_error(error):
        return Base_HTTP_Error_Handling(error, 502)

    @bp.app_errorhandler(503)
    def service_unavailable_error(error):
        return Base_HTTP_Error_Handling(error, 503)

    @bp.app_errorhandler(504)
    def gateway_timeout_error(error):
        return Base_HTTP_Error_Handling(error, 504)

    # Catch-all handler for other unhandled errors
    @bp.app_errorhandler(Exception)
    def unhandled_exception_error(error):
        return Base_HTTP_Error_Handling(error, 500)

    return bp
from flask import Response, request, Blueprint

# from tplink_archer_connection import Stack

from .requests_map import get_response


main = Blueprint('main_bp', __name__)


@main.route('/main/status.htm')
def status_page():
    auth_cookie = 'Authorization=Basic YWRtaW46cGFzc3dvcmQ='    # admin:password
    if request.headers.get('Cookie') == auth_cookie:
        return Response('OK', status=200)
    return Response('Unauthorized', status=403)


@main.route('/cgi/<f>', methods=['GET'])
@main.route('/cgi', methods=['POST'])
def cgi(f=None):
    params = request.url.split('cgi')[1]
    query = request.data.decode('utf-8')
    response = get_response(params, query)
    if not response:
        return Response(status=500)
    return Response(response.get('data'))


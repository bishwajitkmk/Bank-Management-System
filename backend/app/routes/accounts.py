from flask import Blueprint

bp = Blueprint('accounts', __name__)

# TODO: Implement account routes
@bp.route('/test', methods=['GET'])
def test():
    return {'message': 'Accounts route working'}, 200

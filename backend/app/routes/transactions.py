from flask import Blueprint

bp = Blueprint('transactions', __name__)

# TODO: Implement transaction routes
@bp.route('/test', methods=['GET'])
def test():
    return {'message': 'Transactions route working'}, 200

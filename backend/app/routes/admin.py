from flask import Blueprint

bp = Blueprint('admin', __name__)

# TODO: Implement admin routes
@bp.route('/test', methods=['GET'])
def test():
    return {'message': 'Admin route working'}, 200

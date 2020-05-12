import flask
from flask import jsonify, request

from data import *

blueprint = flask.Blueprint('user_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/user')
def get_users():
    session = create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname',
                                    'name', 'age', 'position', 'speciality',
                                    'address', 'email', 'city_from'))
                 for item in users]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname',
                                       'name', 'age', 'position', 'speciality',
                                       'address', 'email', 'city_from'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname',
                  'name', 'age', 'position', 'speciality',
                  'address', 'email', 'city_from']):
        return jsonify({'error': 'Bad request'})
    session = create_session()
    if session.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from']
    )
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    user.surname = request.json.get('surname', user.surname)
    user.name = request.json.get('name', user.name)
    user.age = request.json.get('age', user.age)
    user.position = request.json.get('position', user.position)
    user.speciality = request.json.get('speciality', user.speciality)
    user.address = request.json.get('address', user.address)
    user.email = request.json.get('email', user.email)
    user.city_from = request.json.get('city_from', user.city_from)
    session.merge(user)
    session.commit()
    return jsonify({'success': 'OK'})

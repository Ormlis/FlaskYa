from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from api.resources.parser_user import *
from data import *


def abort_if_user_not_found(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                'user': user.to_dict(only=('id', 'surname',
                                           'name', 'age', 'position', 'speciality',
                                           'address', 'email', 'city_from'))
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = put_parser.parse_args()
        session = create_session()
        user = session.query(User).get(user_id)
        user.surname = args.get('surname', user.surname)
        user.name = args.get('name', user.name)
        user.age = args.get('age', user.age)
        user.position = args.get('position', user.position)
        user.speciality = args.get('speciality', user.speciality)
        user.address = args.get('address', user.address)
        user.email = args.get('email', user.email)
        user.city_from = args.get('city_from', user.city_from)
        session.merge(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'news': [item.to_dict(
            only=('id', 'surname',
                  'name', 'age', 'position', 'speciality',
                  'address', 'email', 'city_from')) for item in users]})

    def post(self):
        args = post_parser.parse_args()
        session = create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

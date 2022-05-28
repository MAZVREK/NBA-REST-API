import sqlite3
from flask_restful import Resource, reqparse

# USER CLASS FOR MAKING NEW USERS
class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    # FINDING METHOD
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    # FINDING METHOD
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

# CLASS FOR CREATING NEW USERS
class UserRegister(Resource):

    # PARSER CREATED FOR CHECKING IF GIVE DATA IS COMPLETE
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )

    # METHOD THAT CREATES USER IN DATABASE
    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        return {'message': 'User created succesfully.'}, 201

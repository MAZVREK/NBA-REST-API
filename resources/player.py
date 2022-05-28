import sqlite3
from flask_restful import  reqparse, Resource
from flask_jwt import jwt_required

# RESOURCE CLASS FOR PLAYER
class Player(Resource):
    # PARSER CREATED FOR CHECKING IF GIVE DATA IS COMPLETE
    parser = reqparse.RequestParser()
    parser.add_argument('team',
                        type=str,
                        required=True,
                        help='This field cannot be left blank!'
                        )
    parser.add_argument('conference',
                        type=str,
                        required=True,
                        help='This field cannot be left blank!'
                        )
    parser.add_argument('division',
                        type=str,
                        required=True,
                        help='This field cannot be left blank!'
                        )
    parser.add_argument('position',
                        type=str,
                        required=True,
                        help='This field cannot be left blank!'
                        )
    parser.add_argument('height',
                        type=str,
                        required=True,
                        help='This field cannot be left blank!'
                        )
    parser.add_argument('age',
                        type=int,
                        required=True,
                        help='This field cannot be left blank!'
                        )
    parser.add_argument('number',
                        type=int,
                        required=True,
                        help='This field cannot be left blank!'
                        )

    # GET METHOD THAT RETURNS A PLAYER IF HE IS IN DATABASE
    def get(self, name):
        player = self.find_by_name(name)
        if player:
            return player
        return {'message': 'Player not found'}, 404

    # HELPING METHOD FOR FINDING PLAYERS IN DATABASE
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM players WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'player': {'name': row[0], 'team': row[1], 'conference': row[2],
             'division': row[3], 'position': row[4], 'height': row[5] ,
             'age': row[6], 'number': row[7]}}

    # POST METHOD FOR ADDING PLAYERS TO DATABASE
    # METHOD REQUIRES JWT TOKEN TO BE USED
    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An player with name {} already exists.".format(name)}, 400
        data = Player.parser.parse_args()
        player = {'name': name, 'team': data['team'], 'conference': data['conference'],
         'division': data['division'], 'position': data['position'], 'height': data['height'] ,
         'age': data['age'], 'number': data['number']}

        try:
            self.insert(player)
        except:
            return {"message": "An error occured during inserting a player into database."}, 500 # Internal server error
        return player, 201

    # HELPING METHOD FOR INSERTING DATA INTO DATBASE
    @classmethod
    def insert(cls, player):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'INSERT INTO players VALUES (?,?,?,?,?,?,?,?)'
        cursor.execute(query, (player['name'], player['team'], player['conference'],
        player['division'], player['position'], player['height'], player['age'], player['number']))

        connection.commit()
        connection.close()

    # DELETE METHOD FOR DELETING PLAYERS FROM DATABASE
    # METHOD REQUIRES JWT TOKEN TO BE USED
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'DELETE FROM players WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {"message": "Player deleted"}

    # PUT METHOD FOR CREATING OR UPDATING PLAYER
    # METHOD REQUIRES JWT TOKEN TO BE USED
    @jwt_required()
    def put(self, name):
        data = Player.parser.parse_args()

        player = self.find_by_name(name)
        updated_player = {'name': name, 'team': data['team'], 'conference': data['conference'],
         'division': data['division'], 'position': data['position'], 'height': data['height'] ,
         'age': data['age'], 'number': data['number']}

        if player is None:
            try:
                self.insert(updated_player)
            except:
                return {'message': "An error has occured during inserting player."}, 500
        else:
            try:
                self.update(updated_player)
            except:
                return {'message': "An error has occured during updating a player."}, 500
        return updated_player

    # HELPING METHOD THAT UPDATES A PLAYER IN DATABASE
    @classmethod
    def update(cls, player):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'UPDATE players SET team=? conference=? division=? position=? height=? age=? number=? WHERE name=?'
        cursor.execute(query, (player['team'], player['conference'],
        player['division'], player['position'], player['height'], player['age'], player['number'], player['name']))

        connection.commit()
        connection.close()


# RESOURCE CLASS FOR PLAYERS LIST
class PlayerList(Resource):

    # GET METHOD FOR GETTING ALL PLAYERS IN DATABASE
    def get(self):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM players'
        result = cursor.execute(query)
        players = []
        for row in result:
            players.append({'name': row[0], 'team': row[1], 'conference': row[2],
             'division': row[3], 'position': row[4], 'height': row[5] ,
             'age': row[6], 'number': row[7]})

        connection.close()
        return {'players': players}

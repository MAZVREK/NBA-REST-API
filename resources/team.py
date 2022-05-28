import sqlite3
from flask_restful import  reqparse, Resource
from flask_jwt import jwt_required

# RESOURCE CLASS FOR TEAM
class Team(Resource):
    # PARSER CREATED FOR CHECKING IF GIVE DATA IS COMPLETE
    parser = reqparse.RequestParser()
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

    # GET METHOD THAT RETURNS A TEAM IF HE IS IN DATABASE
    def get(self, name):
        team = self.find_by_name(name)
        if team:
            return team
        return {'message': 'Team not found'}, 404

    # HELPING METHOD FOR FINDING TEAMS IN DATABASE
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM teams WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'team': {'name': row[0], 'conference': row[1], 'division': row[2]}}

    # POST METHOD FOR ADDING TEAMS TO DATABASE
    # METHOD REQUIRES JWT TOKEN TO BE USED
    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "A team with name {} already exists.".format(name)}, 400
        data = Team.parser.parse_args()
        team = {'name': name, 'conference': data['conference'], 'division': data['division']}

        try:
            self.insert(team)
        except:
            return {"message": "An error occured during inserting a team into database."}, 500 # Internal server error
        return team, 201

    # HELPING METHOD FOR INSERTING DATA INTO DATBASE
    @classmethod
    def insert(cls, team):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'INSERT INTO teams VALUES (?,?,?)'
        cursor.execute(query, (team['name'], team['conference'], team['division']))

        connection.commit()
        connection.close()

    # DELETE METHOD FOR DELETING TEAMS FROM DATABASE
    # METHOD REQUIRES JWT TOKEN TO BE USED
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'DELETE FROM teams WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {"message": "Team deleted"}

    # PUT METHOD FOR CREATING OR UPDATING TEAM
    # METHOD REQUIRES JWT TOKEN TO BE USED
    @jwt_required()
    def put(self, name):
        data = Team.parser.parse_args()

        team = self.find_by_name(name)
        updated_team = {'name': name, 'conference': data['conference'], 'division': data['division']}

        if team is None:
            try:
                self.insert(updated_team)
            except:
                return {'message': "An error has occured during inserting team."}, 500
        else:
            try:
                self.update(updated_team)
            except:
                return {'message': "An error has occured during updating a team."}, 500
        return updated_team

    # HELPING METHOD THAT UPDATES A TEAM IN DATABASE
    @classmethod
    def update(cls, team):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'UPDATE players SET conference=? division=? WHERE name=?'
        cursor.execute(query, (team['conference'], team['division'], team['name']))

        connection.commit()
        connection.close()

# RESOURCE CLASS FOR TEAMS LIST
class TeamList(Resource):

    # GET METHOD FOR GETTING ALL TEAMS IN DATABASE
    def get(self):
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM teams'
        result = cursor.execute(query)
        teams = []
        for row in result:
            teams.append({'team': {'name': row[0], 'conference': row[1], 'division': row[2]}})

        connection.close()
        return {'teams': teams}

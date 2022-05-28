from flask import Flask, request, render_template
from flask_restful import Api
from flask_jwt import JWT
from security.security import identity, authenticate
from security.user import User, UserRegister
from resources.player import Player, PlayerList
from resources.team import Team, TeamList

# CREATING API AND CHANGING JWT AUTH URL FROM /auth TO /login
app = Flask(__name__)
app.secret_key = 'nba'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)

@app.route("/")
def main():
    return render_template('index.html')

# ADDING RESOURCES TO API
api.add_resource(Player, '/player/<string:name>')
api.add_resource(PlayerList, '/players')
api.add_resource(Team, '/team/<string:name>')
api.add_resource(TeamList, '/teams')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)

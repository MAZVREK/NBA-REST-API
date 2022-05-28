# NBA-REST-API

REST API with NBA PLAYERS CREATED IN FLASK

DESCRTIPTION:

CRUD + REST API CREATED IN FLASK USES JWT FOR AUTHORIZATION. GET METHOD DOESNT REQUIRE JWT-TOKEN, OTHERS DO.
INSERTED PLAYERS HAVE SPACE BETWEEN FIRSTNAME AND LASTNAME SO THOSE NEED TO BE SEPARATED IN REQUEST, EXAMPLE 
REST-API REQUEST 127.0.0.1:5000/player/Trae Young


ENDPOINTS:

  - /teams - return json of all teams

  - /team/<name> - return json of team with that name

  - /players - return json of all players

  - /player/<name> - return json of player with that name

  - /login - used for login, return JWT-TOKEN upon succesfull login

  - /register - used for registration


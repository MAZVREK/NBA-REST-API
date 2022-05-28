import sqlite3

connection = sqlite3.connect('database.db')

# CREATES A USERS TABLE IF IT DOESNT EXISTS
cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# CREATES A PLAYERS TABLE IF IT DOESNT EXISTS
create_table = "CREATE TABLE IF NOT EXISTS players (name text, team text, conference text, division text, position text, height text, age int, number int)"
cursor.execute(create_table)
query = "INSERT INTO players VALUES (?,?,?,?,?,?,?,?)"

# LIST OF PLAYERS THAT ARE ADDED UPON A CREATION OF DATABASE
players = [
('Trae Young', 'Atlanta Hawks', 'Eastern', 'Southeast', 'G', "6'1", 23, 11),
('Luka Doncic', 'Dallas Mavericks', 'Western', 'Southwest', 'F', "6'7", 23, 77),
('LeBron James', 'Los Angeles Lakers', 'Western', 'Pacific', 'F', "6'9", 37, 6),
('Ja Morant', 'Memphis Grizzlies', 'Western', 'Southwest', 'G', "6'3", 22, 12),
('Giannis Antetokounmpo', 'Milwaukee Bucks', 'Eastern', 'Central', 'F', "6'11", 27, 34)
]

# ADDS PLAYERS TO PLAYER TABLE
for player in players:
    cursor.execute(query, player)

# CREATES A TEAMS TABLE IF IT DOESNT EXISTS
create_table = "CREATE TABLE IF NOT EXISTS teams (name text, conference text, division text)"
cursor.execute(create_table)
query = "INSERT INTO teams VALUES (?,?,?)"

# LIST OF TEAMS THAT ARE ADDED UPON A CREATION OF DATABASE
teams = [
('Atlanta Hawks', 'Eastern', 'Southeast'),
('Dallas Mavericks', 'Western', 'Southwest'),
('Los Angeles Lakers', 'Western', 'Pacific'),
('Memphis Grizzlies', 'Western', 'Southwest'),
('Milwaukee Bucks', 'Eastern', 'Central')
]

# ADDS TEAMS TO PLAYER TABLE
for team in teams:
    cursor.execute(query, team)

connection.commit()
connection.close()

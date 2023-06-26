import database

def get_player_win_rate(name):
    player = database.get_player(name)
    if player == []:
        return None
    
    wins = player[0][1]
    losses = player[0][2]
    win_rate = round(wins/(wins+losses)*100, 2)
    return win_rate

def get_team_win_rate(name_1, name_2):
    team = database.get_team(name_1, name_2)
    if team == []:
        return None
    
    wins = team[0][2]
    losses = team[0][3]
    win_rate = round(wins/(wins+losses)*100, 2)
    return win_rate

def get_best_team():
    val = database.get_best_team()
    return val[0][0], val[0][1], get_team_win_rate(val[0][0], val[0][1])

def get_worst_team():
    val = database.get_worst_team()
    return val[0][0], val[0][1], get_team_win_rate(val[0][0], val[0][1])
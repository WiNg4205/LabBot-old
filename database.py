import sqlite3


def initialise_db():
    connection = sqlite3.connect("scores.db")
    cursor = connection.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS individual_scores (
        name TEXT NOT NULL,
        wins INTEGER,
        losses INTEGER
    )"""

    sql2 = """
    CREATE TABLE IF NOT EXISTS team_scores (
        name_1 TEXT NOT NULL,
        name_2 TEXT NOT NULL,
        wins INTEGER,
        losses INTEGER
    )"""

    cursor.execute(sql)
    cursor.execute(sql2)

    connection.close()


def add_player(name):
    connection = sqlite3.connect("scores.db")
    cursor = connection.cursor()

    sql = "INSERT INTO individual_scores VALUES(:n, 0, 0)"
    cursor.execute(sql, {"n": name})
    connection.commit()

    connection.close()


def get_player(name):
    connection = sqlite3.connect("scores.db")
    cursor = connection.cursor()

    sql = """
    SELECT *
    FROM individual_scores
    WHERE name = :n
    """
    cursor.execute(sql, {"n": name})
    val = cursor.fetchall()

    connection.close()
    return val


def get_team(name_1, name_2):
    connection = sqlite3.connect("scores.db")
    cursor = connection.cursor()

    sql = """
    SELECT *
    FROM team_scores
    WHERE (name_1 = :n1 AND name_2 = :n2)
        OR (name_1 = :n2 AND name_2 = :n1)
    """
    
    cursor.execute(sql, {"n1": name_1, "n2": name_2})
    val = cursor.fetchall()

    connection.close()

    return val


def update_team_scores(name_1, name_2, wins, losses):
    connection = sqlite3.connect("scores.db")
    cursor = connection.cursor()

    val = get_team(name_1, name_2)
    team = (name_1, name_2, wins, losses)
    # If team doesn't exist
    if val == []:
        cursor.execute("INSERT INTO team_scores VALUES(?,?,?,?)", team)
        connection.commit()
    else:
        wins += val[0][2]
        losses += val[0][3]
        
        sql = """
        UPDATE team_scores
        SET wins = :w, losses = :l
        WHERE (name_1 = :n1 AND name_2 = :n2)
            OR (name_1 = :n2 AND name_2 = :n1)
        """
        
        cursor.execute(sql, {"w": wins, "l": losses, "n1": name_1, "n2": name_2})
        connection.commit()

    connection.close()


def update_individual_scores(name_1, name_2, wins, losses):
    connection = sqlite3.connect("scores.db")
    cursor = connection.cursor()

    val_1 = list(get_player(name_1)[0])
    val_2 = list(get_player(name_2)[0])
    vals = [val_1, val_2]
    for v in vals:
        v[1] += wins
        v[2] += losses

    
    sql = """
    UPDATE individual_scores
    SET wins = :w, losses = :l
    WHERE name = :n
    """
    for val in vals:
        cursor.execute(sql, {"w": val[1], "l": val[2], "n": val[0]})
        connection.commit()
        
    connection.close()


def get_best_team():
    connection = sqlite3.connect("scores.db")
    cursor = connection.cursor()

    sql = """
    SELECT name_1, name_2, (CAST(wins AS FLOAT)/CAST((wins+losses) AS FLOAT))*100 AS win_rate
    FROM team_scores
    ORDER BY win_rate DESC
    LIMIT 1;
    """

    cursor.execute(sql)
    val = cursor.fetchall()
    return val


def get_worst_team():
    connection = sqlite3.connect("scores.db")
    cursor = connection.cursor()

    sql = """
    SELECT name_1, name_2, (CAST(wins AS FLOAT)/CAST((wins+losses) AS FLOAT))*100 AS win_rate
    FROM team_scores
    ORDER BY win_rate ASC
    LIMIT 1;
    """

    cursor.execute(sql)
    val = cursor.fetchall()
    return val
#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error!!")

def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE matches CASCADE;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()
    c.execute("SELECT count(*) FROM players;")
    result = c.fetchone()
    DB.close()
    return int(result[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    c.execute("INSERT INTO players (full_name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()
    c.execute("SELECT DISTINCT players.id, players.full_name, "
              "(SELECT COUNT(*) "
              "FROM matches WHERE players.id = matches.winner_id) "
              "AS wins,"
              " (SELECT COUNT(*) "
              "FROM matches WHERE players.id = matches.winner_id "
              "OR players.id = matches.loser_id) AS allmatches "
              "FROM players "
              "ORDER BY wins DESC")

    result = c.fetchall()
    DB.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()
    c.execute("INSERT INTO matches (winner_id,loser_id)"
              " VALUES (%s,%s)", (winner, loser,))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    currentStandings = playerStandings()
    swissPairings = []
    for i in xrange(1, len(currentStandings), 2):
        swissPairings.append((currentStandings[i - 1][0],
                              currentStandings[i - 1][1],
                              currentStandings[i][0],
                              currentStandings[i][1]))

    return swissPairings

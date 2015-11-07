"""
This module contains functions that can be called to perform various
actions for the implementation of a Swiss-system tournament.
"""

#!/usr/bin/env python

import math
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def runSimpleQuery(query, params=None):
    """Simple convenience method to run the specified query.

    Args:
      query: the query to run
      params: optional parameters to run when executing the query
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()



def deleteMatches():
    """Remove all the match records from the database."""
    runSimpleQuery('DELETE FROM tbl_matches;')


def deletePlayers():
    """Remove all the player records from the database."""
    runSimpleQuery('DELETE FROM tbl_players;')


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    query = 'SELECT count(player_id) as num FROM tbl_players;'
    cursor.execute(query)
    rows = cursor.fetchone()
    conn.close()
    return rows[0]


def countGamesPerRound():
    """Returns the number of games per round."""
    return int(math.ceil(countPlayers() / 2))


# Source for determining number of rounds:
# http://www.wizards.com/dci/downloads/swiss_pairings.pdf
def countRounds():
    """Returns the number of rounds necessary for the tournament."""
    num_players = countPlayers()
    if num_players == 0:
        return 0
    elif num_players == 2:
        return 1
    elif num_players <= 4:
        return 2
    elif num_players <= 8:
        return 3
    elif num_players <= 16:
        return 4
    elif num_players <= 32:
        return 5
    elif num_players <= 64:
        return 6
    elif num_players <= 128:
        return 7
    elif num_players <= 226:
        return 8
    elif num_players <= 409:
        return 9
    else:
        return 10


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
    """
    runSimpleQuery('INSERT INTO tbl_players (name) values (%s);', (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list is the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    query_get_wins = '''SELECT count(match_id)
        FROM view_all_matches
        WHERE winner_id=tbl_players.player_id'''
    query_all_matches = '''SELECT count(match_id)
        FROM view_all_matches
        WHERE winner_id=tbl_players.player_id
            OR loser_id=tbl_players.player_id'''
    query = '''SELECT player_id as id, name,
            (''' + query_get_wins + ''') as wins,
            (''' + query_all_matches + ''') as matches
        FROM tbl_players
        ORDER BY wins desc;'''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def playerRecord(player_id):
    """Returns a list of a player's win/loss record.

    Args:
      player_id: the id number of the player whose record should be retrieved

    Returns:
      A tuple which contains (wins, losses)
    """
    conn = connect()
    cursor = conn.cursor()
    query_get_wins = '''SELECT count(match_id)
        FROM view_all_matches
        WHERE winner_id=''' + str(player_id)
    query_get_losses = '''SELECT count(match_id)
        FROM view_all_matches
        WHERE loser_id=''' + str(player_id)
    query = '''SELECT
            (''' + query_get_wins + ''') as wins,
            (''' + query_get_losses + ''') as losses
        FROM tbl_players
        WHERE player_id=''' + str(player_id) + '''
        ORDER BY wins desc;'''
    cursor.execute(query)
    results = cursor.fetchone()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    runSimpleQuery('''INSERT INTO tbl_matches (winner_id, loser_id)
        values (%s, %s);''', (winner, loser,))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ranked_players = playerStandings()
    counter = 0
    results = []
    for num in range(0, countGamesPerRound()):
        player_1 = ranked_players[counter]
        player_2 = ranked_players[counter + 1]
        results.append((player_1[0], player_1[1], player_2[0], player_2[1]))
        counter += 2
    return results



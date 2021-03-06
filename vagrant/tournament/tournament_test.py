"""
This module contains test cases for tournament.py, testing various
aspects of the implementation of a Swiss-system tournament.
"""

#!/usr/bin/env python

import random
from tournament import *

def testDeleteMatches():
    """Test to delete all old matches."""
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    """Test to delete all players."""
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    """Test to count the number of players after having deleted them."""
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    """Test to register a player and retrieve player count."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    """Test to register and count players, then delete and re-count."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    """Test to check for valid player standings before matches."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    """Test to report matches and validate accurate player standings."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    """Test to validate correct pairings of players based on records."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def simulateFullTournament():
    """Creates and simulates a tournament of 16 players.

    Fun Fact: Players names are characters from 4 of my favorite TV
    shows: White Collar, Seinfeld, Castle, and Burn Notice.
    """
    deleteMatches()
    deletePlayers()
    all_players = ["Neal Caffrey", "Peter Burke",
                   "Mozzie", "Clinton Jones",
                   "Jerry Seinfeld", "George Costanza",
                   "Elaine Benes", "Cosmo Kramer",
                   "Richard Castle", "Kate Beckett",
                   "Javier Esposito", "Kevin Ryan",
                   "Michael Westen", "Sam Axe",
                   "Fiona Glenanne", "Jesse Porter"]
    for player in all_players:
        registerPlayer(player)
    num_rounds = countRounds()

    print "\nIT'S TOURNAMENT TIME!\n------------------------\n"
    print "Number of Players: {0}\nNumber of Rounds: {1}".format(
        len(all_players), num_rounds
    )

    # Loop over rounds, create matchups, generate random winner, report match
    for num in range(0, num_rounds):
        print "\nROUND #{0}\n------------------------".format(num + 1)
        pairings = swissPairings()
        match_num = 1
        for pair in pairings:
            rand = int(round(random.randint(0, 1)))
            # Guard against winner being the "Bye", even though this is
            # already guarded against in reportMatch() in tournament.py
            winner = (pair[0], pair[1]) if rand == 0 or pair[2] is -1 \
                else (pair[2], pair[3])
            loser = (pair[0], pair[1]) if rand == 1 and pair[2] is not -1 \
                else (pair[2], pair[3])
            winner_record = playerRecord(winner[0])
            loser_record = playerRecord(loser[0])
            print "  > Match {0}: {1} ({2}-{3}) vs. {4} ({5}-{6})".format(
                match_num,
                winner[1], winner_record[0], winner_record[1],
                loser[1], loser_record[0], loser_record[1]
            )
            reportMatch(winner[0], loser[0])
            match_num += 1

    # Get final standings
    standings = playerStandings()
    print "\nFINAL STANDINGS\n------------------------"
    rank = 1
    for player in standings:
        player_record = playerRecord(player[0])
        print "  {0}. {1} ({2}-{3})".format(
            rank, player[1], player_record[0], player_record[1]
        )
        rank += 1
    print " "


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
    simulateFullTournament()

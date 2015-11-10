-- Database and table definitions for the Tournament Results project.

-- Source for dropping DB if there are active connections:
-- http://stackoverflow.com/a/5408501/1914233
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
    AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE IF NOT EXISTS tbl_players (
    player_id serial PRIMARY KEY,
    name text NOT NULL
);

-- Note: No foreign key reference used for loser_id, as current solution
-- for supporting an odd number of players uses value of -1 for loser_id
-- which is not a legit serial value to any player in tbl_players.
CREATE TABLE IF NOT EXISTS tbl_matches (
    match_id serial PRIMARY KEY,
    winner_id integer REFERENCES tbl_players (player_id) ON DELETE CASCADE,
    loser_id integer,
    CHECK (winner_id <> loser_id)
);

CREATE VIEW view_player_standings AS
    SELECT player_id as id, name,
    (SELECT count(*) FROM tbl_matches
        WHERE winner_id=tbl_players.player_id) as wins,
    (SELECT count(*) FROM tbl_matches
        WHERE loser_id=tbl_players.player_id) as losses,
    (SELECT count(*) FROM tbl_matches
        WHERE winner_id=tbl_players.player_id
            OR loser_id=tbl_players.player_id) as matches
    FROM tbl_players;

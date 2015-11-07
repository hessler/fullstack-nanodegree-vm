-- Database and table definitions for the Tournament Results project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE IF NOT EXISTS tbl_players (
    player_id serial PRIMARY KEY,
    name text
);

CREATE TABLE IF NOT EXISTS tbl_matches (
    match_id serial PRIMARY KEY,
    winner_id integer REFERENCES tbl_players (player_id),
    loser_id integer REFERENCES tbl_players (player_id)
);

CREATE VIEW view_all_matches AS 
    SELECT * FROM tbl_matches

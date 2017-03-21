-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create tournament database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- create players table
CREATE TABLE players ( id SERIAL primary key,
                       full_name TEXT,
                       time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      );

-- create matches table
CREATE TABLE matches ( id SERIAL primary key,
                       winner_id integer references players(id),
                       loser_id integer references players(id),
                       time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      );


-- Create and select the database
CREATE DATABASE IF NOT EXISTS ipl_analytics;
USE ipl_analytics;

-- Drop existing tables if re-running script
DROP TABLE IF EXISTS ipl_cleaned_master;
DROP TABLE IF EXISTS ipl_master;

-- Schema for raw imported master table
CREATE TABLE ipl_master (
    match_id INT,
    season VARCHAR(50),
    venue VARCHAR(255),
    toss_winner VARCHAR(100),
    toss_decision VARCHAR(50),
    batter VARCHAR(100),
    bowler VARCHAR(100),
    runs_batter INT,
    runs_extras INT,
    runs_total INT,
    match_won_by VARCHAR(100),
    player_of_match VARCHAR(100)
);

-- Schema for cleaned master table (populated via Python data cleaning script)
CREATE TABLE ipl_cleaned_master (
    match_id INT,
    season VARCHAR(50),
    venue VARCHAR(255),
    toss_winner VARCHAR(100),
    toss_decision VARCHAR(50),
    batter VARCHAR(100),
    bowler VARCHAR(100),
    runs_batter INT,
    runs_extras INT,
    runs_total INT,
    match_won_by VARCHAR(100),
    player_of_match VARCHAR(100)
);
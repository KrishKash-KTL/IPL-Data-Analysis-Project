USE ipl_analytics;

-- Query 1: Top 10 Run-Scorers in the Dataset
SELECT batter, SUM(runs_batter) AS total_runs
FROM ipl_cleaned_master
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;

-- Query 2: Most Player of the Match Awards
SELECT player_of_match, COUNT(DISTINCT match_id) AS total_awards
FROM ipl_cleaned_master
WHERE player_of_match IS NOT NULL AND player_of_match != 'Unknown'
GROUP BY player_of_match
ORDER BY total_awards DESC
LIMIT 10;

-- Query 3: Match Wins Breakdown by Team
SELECT match_won_by, COUNT(DISTINCT match_id) AS matches_won
FROM ipl_cleaned_master
WHERE match_won_by IS NOT NULL AND match_won_by != 'Unknown'
GROUP BY match_won_by
ORDER BY matches_won DESC;

-- Query 4: Toss Decision Impact on Match Outcomes
SELECT toss_decision, COUNT(DISTINCT match_id) AS total_matches
FROM ipl_cleaned_master
GROUP BY toss_decision;
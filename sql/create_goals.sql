USE bundesliga;

CREATE TABLE goals (
	goal_id INT PRIMARY KEY,
    match_id INT NOT NULL,	
    team_code INT NOT NULL,	
    scorer_name	 VARCHAR (100) NOT NULL, 
    scorer_code	 INT NOT NULL,
    `minute`  INT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(WS_match_id),
    FOREIGN KEY (team_code) REFERENCES teams(team_code)
);

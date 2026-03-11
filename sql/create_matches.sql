USE bundesliga;

CREATE TABLE matches (
	WS_match_id INT PRIMARY KEY,
	Match_name	VARCHAR (100) NOT NULL,
    MD INT, 	
    `Day`	VARCHAR (20), 
    `Date` DATE NOT NULL,	
    `Time`	TIME NOT NULL,
    venue	VARCHAR (100) NOT NULL,
    Attendance INT,
	refereeCode INT, 
	Weather		VARCHAR (20), 
	home_Team_Code INT NOT NULL, 
	away_Team_Code INT NOT NULL, 
	Result	VARCHAR (20) NOT NULL,
    halftime_score	VARCHAR (20) NOT NULL,	
    halftime_score_HT	INT NOT NULL,
	halftime_score_AT	INT NOT NULL,
    Score	VARCHAR (20) NOT NULL,		
    HT_score	INT NOT NULL,	
    AT_score	INT NOT NULL,
    FOREIGN KEY (refereeCode) REFERENCES referees(ref_code),
    FOREIGN KEY (home_Team_Code) references teams(team_code),
    FOREIGN KEY (away_Team_Code) references teams(team_code)
);

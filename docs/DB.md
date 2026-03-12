# DB

## Sample data

[Sample data can be found here](https://github.com/W-ren-P/bundesliga-analytics/tree/main/sample_data)

The following files contain the full data used in the main site:

- referees.csv
- table.csv
- teams.csv
- teams_info.csv

The following files contain only sample data:

- sample_data_goals.csv
- sample_data_main.csv
- sample_data_match_cum_agg_stats.csv
- sample_data_matches.csv
- sample_data_team_match_stats.csv


## Example Python scripts

All bar one of the smaller csv files can be created from the "sample_data_main.csv" file with this simple Python script:

```python
import pandas as pd
import os

file_to_read = "sample_data_main.csv"
folder_to_read = yourfolder
file_to_save = "youroutputfilename.csv"

cols_to_use = [yourcolumnstouse]
os.chdir(folder_to_read)

df = pd.read_csv(file_to_read, index_col = False, encoding = "cp1252")
df = df[cols_to_use]
df.drop_duplicates(inplace = True)
df.to_csv(file_to_save, index=False, encoding = "utf8")
```

Creating the sample_data_goals.csv file requires this Python script:

```python
import pandas as pd
import os

file_to_read = "sample_data_main.csv"
folder_to_read = yourfolder
file_to_save = "sample_data_goals.csv"

os.chdir(folder_to_read)
df = pd.read_csv(file_to_read, index_col = False)

df_ht = df[df['HTorAT'] == 'HT'].copy()
all_goals = []

for i in range(1, 11):

    ht_goals = df_ht[[
        'WS_match_id',
        'home_Team_Code',
        f'HT_goalscorers_{i}',
        f'HT_goalscorers_{i}_code',
        f'HT_goal_mins_{i}'
    ]].copy()
    ht_goals.columns = ['match_id', 'team_code', 'scorer_name', 'scorer_code', 'minute']

    at_goals = df_ht[[
        'WS_match_id',
        'away_Team_Code',
        f'AT_goalscorers_{i}',
        f'AT_goalscorers_{i}_code',
        f'AT_goal_mins_{i}'
    ]].copy()
    at_goals.columns = ['match_id', 'team_code', 'scorer_name', 'scorer_code', 'minute']

    all_goals.append(ht_goals)
    all_goals.append(at_goals)

goals_df = pd.concat(all_goals, ignore_index=True)
goals_df = goals_df.dropna(subset=['scorer_name'])
goals_df = goals_df.sort_values(['match_id', 'minute']).reset_index(drop=True)
goals_df.insert(0, 'goal_id', range(1, len(goals_df) + 1))

goals_df.to_csv(file_to_save, index=False)
```

## Example SQL queries

Create goals table:

```sql
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
```


Create matches table:

```sql
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
```


Create team_match_stats table:

```sql
CREATE TABLE team_match_stats (
	WS_id_primary_key VARCHAR (50) PRIMARY KEY,
	match_id INT NOT NULL, 
	Team_Code INT NOT NULL, 
    Team_result	VARCHAR (50),
    Team_points	INT,
    Team_Goals	INT NOT NULL, 
    Opp_Goals	INT NOT NULL, 
    HTorAT VARCHAR (30) NOT NULL,
    manager VARCHAR (100),

	Shots INT,
	Shots_on_target INT,
	Pass_Success_percent INT,
	Aerial_Duel_Success_percent INT,
	Dribbles_won INT,
	Tackles INT,
	Possession_percent INT,
	Total_Attempts INT,
	Goals INT,
	Conversion_Rate_percent INT,
	Open_Play_shots INT,
	Set_Piece_shots INT,
	Counter_Attack_shots INT,
	Penalty_shots INT,
	Own_Goal_shots INT,
	Total_Passes INT,
	Crosses INT,
	Through_Balls INT,
	Long_Balls INT,
	Short_Passes INT,
	Average_Pass_Streak INT,
	Total_Cards INT,
	Cards_for_Fouls INT,
	Cards_for_Unprofessional INT,
	Cards_for_Dives INT,
	Cards_for_Other INT,
	Red_Cards INT,
	Yellow_Cards INT,
	Cards_per_Foul_percent INT,
	Fouls_per_Game INT,
	Ratings FLOAT,
	Total_Shots INT,
	Woodwork_shots INT,
	Shots_on_target_B INT,
	Shots_off_target INT,
	Shots_blocked INT,
	Possession_percent_b INT,
	Touches INT,
	Pass_Success_percent_b INT,
	Total_passes_b INT,
	Accurate_passes INT,
	Key_passes INT,
	Dribbles_Won_b INT,
	Dribbles_attempted INT,
	Dribbled_past INT,
	Dribble_Success_percent INT,
	Aerials_Won INT,
	Aerials_Won_percent INT,
	Offensive_Aerials INT,
	Defensive_Aerials INT,
	Successful_Tackles INT,
	Tackles_Attempted INT,
	Was_Dribbled INT,
	Tackle_Success_percent INT,
	Clearances INT,
	Interceptions INT,
	Corners INT,
	Corner_Accuracy_percent INT,
	Dispossessed INT,
	`Errors` INT,
	Fouls INT,
	Offsides INT,
	Goals_b INT,
	Shots_on_Target_c INT,
	Shots_off_Target_b INT,
	Woodworks_shots INT,
	Blocked_shots INT,
	Own_shots INT,
	`6_yard_box_shots` INT,
	Penalty_Area_shots INT,
	Outside_of_box_shots INT,
	Open_Play_shots_b INT,
	Fastbreak_shots_b INT,
	Set_Pieces_shots_b INT,
	Penalty_shots_b INT,
	Own_Goal_shots_b INT,
	Right_foot_shots INT,
	Left_foot_shots INT,
	Headed_shots INT,
	Crossed_passes INT,
	Freekick_passes INT,
	Corner_passes INT,
	Through_Balls_b INT,
	Throw_Ins INT,
	Key_Passes_b INT,
	Long_passes_b INT,
	Short_passes_b INT,
	Chipped_passes INT,
	Ground_passes INT,
	Headed_passes INT,
	Feet_passes INT,
	Forward_passes INT,
	Backward_passes INT,
	Passes_to_Left INT,
	Passes_to_Right INT,
	Defensive_Third_passes INT,
	Mid_Third_passes INT,
	Final_Third_passes INT,
	Successful_passes_b INT,
	Unsuccessful_passes_b INT,
	Successful_Tackles_b INT,
	Was_Dribbled_b INT,
	Interceptions_b INT,
	Total_clearances INT,
	clearances_Off_The_Line INT,
	clearances_with_Head INT,
	clearances_with_Feet INT,
	Blocked_Shots_c INT,
	blocked_Crosses INT,
	Offsides_b INT,
	Fouls_b INT,
	Aerial_duels_b INT,
	Touches_b INT,
	Dispossessed_b INT,
	Turnover INT,
	error_Lead_to_Shot INT,
	error_Lead_to_Goal INT,
	Saves INT,
	Claims INT,
	Punches INT,
    
    FOREIGN KEY (match_id) references matches(WS_match_id),
    FOREIGN KEY	(Team_Code) references teams(team_code)
);
```


Create match_cum_agg_stats (ie. cumulative & aggregate match stats) table:

```sql
CREATE TABLE match_cum_agg_stats (
	WS_match_id INT PRIMARY KEY,

	totalGoals INT,
	totalShots INT,
	totalShots_on_target INT,
	totalPass_Success_percent INT,
	totalDribbles_won INT,
	totalTackles INT,
	totalTotal_Attempts INT,
	totalGoalsB INT,
	totalConversion_Rate_percent INT,
	totalOpen_Play_shots INT,
	totalSet_Piece_shots INT,
	totalCounter_Attack_shots INT,
	totalPenalty_shots INT,
	totalOwn_Goal_shots INT,
	totalTotal_Passes INT,
	totalCrosses INT,
	totalThrough_Balls INT,
	totalLong_Balls INT,
	totalShort_Passes INT,
	totalAverage_Pass_Streak INT,
	totalTotal_Cards INT,
	totalCards_for_Dives INT,
	totalRed_Cards INT,
	totalYellow_Cards INT,
	totalWoodwork_shots INT,
	totalShots_off_target INT,
	totalShots_blocked INT,
	totalTouches INT,
	totalAccurate_passes INT,
	totalKey_passes INT,
	totalDribbles_attempted INT,
	totalDribble_Success_percent INT,
	totalAerials INT,
	totalTackles_Attempted INT,
	totalTackle_Success_percent INT,
	totalClearances INT,
	totalInterceptions INT,
	totalCorners INT,
	totalCorner_Accuracy_percent INT,
	totalDispossessed INT,
	totalErrors INT,
	totalFouls INT,
	totalOffsides INT,
	`total6_yard_box_shots` INT,
	totalPenalty_Area_shots INT,
	totalOutside_of_box_shots INT,
	totalRight_foot_shots INT,
	totalLeft_foot_shots INT,
	totalHeaded_shots INT,
	totalFreekick_passes INT,
	totalThrow_Ins INT,
	totalChipped_passes INT,
	totalGround_passes INT,
	totalHeaded_passes INT,
	totalFeet_passes INT,
	totalForward_passes INT,
	totalBackward_passes INT,
	totalPasses_to_Left INT,
	totalPasses_to_Right INT,
	totalDefensive_Third_passes INT,
	totalMid_Third_passes INT,
	totalFinal_Third_passes INT,
	totalclearances_Off_The_Line INT,
	totalclearances_with_Head INT,
	totalclearances_with_Feet INT,
	totalblocked_Crosses INT,
	totalTurnover INT,
	totalerror_Lead_to_Shot INT,
	totalerror_Lead_to_Goal INT,
	totalSaves INT,
	totalClaims INT,
	totalPunches INT,
	percentHT_ShotsOffTarget FLOAT,
	percentHT_ShotsOnTarget FLOAT,
	percentHT_ShotsBlocked FLOAT,
	percentHT_6ydBoxShots FLOAT,
	percentHT_PenAreaShots FLOAT,
	percentHT_OutsideBoxShots FLOAT,
	percentHT_OpenPlayShots FLOAT,
	percentHT_FastBreakShots FLOAT,
	percentHT_SetPieceShots FLOAT,
	percentHT_RightFootedShots FLOAT,
	percentHT_LeftFootedShots FLOAT,
	percentHT_HeadedShots FLOAT,
	percentHT_LongPasses FLOAT,
	percentHT_ShortPasses FLOAT,
	percentHT_HighPasses FLOAT,
	percentHT_LowPasses FLOAT,
	percentHT_HeadPasses FLOAT,
	percentHT_FeetPasses FLOAT,
	percentHT_ForwardPasses FLOAT,
	percentHT_BackwardPasses FLOAT,
	percentHT_PassesToLeft FLOAT,
	percentHT_PassesToRight FLOAT,
	percentHT_DefThirdPasses FLOAT,
	percentHT_MidThirdPasses FLOAT,
	percentHT_FinalThirdPasses FLOAT,
	percentAT_ShotsOffTarget FLOAT,
	percentAT_ShotsOnTarget FLOAT,
	percentAT_ShotsBlocked FLOAT,
	percentAT_6ydBoxShots FLOAT,
	percentAT_PenAreaShots FLOAT,
	percentAT_OutsideBoxShots FLOAT,
	percentAT_OpenPlayShots FLOAT,
	percentAT_FastBreakShots FLOAT,
	percentAT_SetPieceShots FLOAT,
	percentAT_RightFootedShots FLOAT,
	percentAT_LeftFootedShots FLOAT,
	percentAT_HeadedShots FLOAT,
	percentAT_LongPasses FLOAT,
	percentAT_ShortPasses FLOAT,
	percentAT_HighPasses FLOAT,
	percentAT_LowPasses FLOAT,
	percentAT_HeadPasses FLOAT,
	percentAT_FeetPasses FLOAT,
	percentAT_ForwardPasses FLOAT,
	percentAT_BackwardPasses FLOAT,
	percentAT_PassesToLeft FLOAT,
	percentAT_PassesToRight FLOAT,
	percentAT_DefThirdPasses FLOAT,
	percentAT_MidThirdPasses FLOAT,
	percentAT_FinalThirdPasses FLOAT,

    FOREIGN KEY (WS_match_id) references matches(WS_match_id)
);
```


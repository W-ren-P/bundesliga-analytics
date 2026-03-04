
from flask import Flask, jsonify, render_template, request
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

app = Flask(__name__)
# engine = create_engine('mysql+pymysql://root:fe11ini07@localhost/bundesliga')
# engine = create_engine('mysql+pymysql://root:gKfjDindMHctXqUDOpnkRIPGkWxYfSTh@tramway.proxy.rlwy.net:52998/railway')
# engine = create_engine(
#     'postgresql://postgres.vhznhbmqjigmjbwporfc:tPZ8edeuvBtciFqV@aws-1-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require'
# )
# engine = create_engine(
#     'postgresql://postgres.vhznhbmqjigmjbwporfc:tPZ8edeuvBtciFqV@aws-1-eu-west-1.pooler.supabase.com:5432/postgres?sslmode=require'
# )
database_path = '/home/WrenP/my_database.db'
engine = create_engine(f'sqlite:///{database_path}')


@app.route('/')
def home():
#     query = """
#         SELECT scorer_name, scorer_code, COUNT(*) AS goal_count
#         FROM goals
#         WHERE minute < 15
#         GROUP BY scorer_name, scorer_code
#         ORDER BY goal_count DESC
#         LIMIT 10
#     """
#     df = pd.read_sql(query, engine)
#     # Convert data to a list of dictionaries for the template
#     scorers_data = df.to_dict(orient='records')
#     return render_template('index.html', scorers=scorers_data)
    return render_template('index.html')


# @app.route('/top-scorers')
# def top_scorers():
# ##    engine = create_engine('mysql+pymysql://root:fe11ini07@localhost/bundesliga')
#     query = """
#         SELECT scorer_name, scorer_code, COUNT(*) AS goal_count
#         FROM goals
#         WHERE minute < 15
#         GROUP BY scorer_name, scorer_code
#         ORDER BY goal_count DESC
#         LIMIT 10
#     """
#     df = pd.read_sql(query, engine)
#     data = df.to_dict(orient='records')
# ##    return jsonify(df.to_dict(orient='records'))
#     return render_template('index.html', scorers=data)
@app.route('/top-scorers')
def top_scorers():
    # 1. Get the 'minutes' value from the URL (default to 15 if not found)
    selected_mins = request.args.get('minutes', default=15, type=int)

    # 2. Use the variable in your SQL query
    query = f"""
        SELECT scorer_name, COUNT(*) AS goal_count
        FROM goals
        WHERE minute < :mins
        GROUP BY scorer_name
        ORDER BY goal_count DESC
        LIMIT 15
    """

    # 3. Pass the variable into the execute command
    df = pd.read_sql(query, engine, params={'mins': selected_mins})

    data = df.to_dict(orient='records')
        # return render_template('index.html', scorers=data)
    return render_template('index.html', scorers=data, current_mins=selected_mins)

@app.route('/referees-cards-total')
def referees_cards_total():
    query = """
        SELECT referees.ref_name, SUM(match_cum_agg_stats.totalTotal_Cards) AS card_count
        FROM match_cum_agg_stats

        JOIN matches ON match_cum_agg_stats.WS_match_id = matches.WS_match_id
        JOIN referees ON referees.ref_code = matches.refereeCode

        GROUP BY referees.ref_code, referees.ref_name
        ORDER BY card_count DESC;
    """
    df = pd.read_sql(query, engine)
    data = df.to_dict(orient='records')
##    return jsonify(df.to_dict(orient='records'))
    return render_template('index.html', referees=data)

@app.route('/referees-cards-average')
def referees_cards_average():
    query = """
        SELECT referees.ref_name,
               SUM(match_cum_agg_stats.totalTotal_Cards) AS total_cards,
               COUNT(match_cum_agg_stats.WS_match_id) AS games_refereed,
               ROUND(SUM(match_cum_agg_stats.totalTotal_Cards) * 1.0 / COUNT(match_cum_agg_stats.WS_match_id), 2) AS cards_per_game
        FROM match_cum_agg_stats
        JOIN matches ON match_cum_agg_stats.WS_match_id = matches.WS_match_id
        JOIN referees ON referees.ref_code = matches.refereeCode
        GROUP BY referees.ref_code, referees.ref_name
        ORDER BY cards_per_game DESC;
    """
    df = pd.read_sql(query, engine)
    data = df.to_dict(orient='records')
##    return jsonify(df.to_dict(orient='records'))
    return render_template('index.html', referees=data)

@app.route('/db-status')
def db_status():
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    status = []
    for table in tables:
        # Get row count for each table
        count = pd.read_sql(f"SELECT COUNT(*) FROM {table}", engine).iloc[0, 0]
        status.append({
            "table_name": table,
            "row_count": int(count)
        })

    return jsonify({
        "database": "my_database.db",
        "tables": status,
        "location": database_path
    })


@app.route('/teams')
def teams_home():
    # teams = ['Bremen', 'Bayern', 'Leverkusen', 'Leipzig', 'Wolfsburg', 'Heidenheim', 'Hoffenheim', 'Freiburg', 'Augsburg','Gladbach',
    # 'Stuttgart', 'Bochum', 'Dortmund', 'Cologne', 'Union', 'Mainz', 'Frankfurt', 'Darmstadt']
    teams = [
        "Bremen", "Bayern", "Leverkusen", "Leipzig", "Wolfsburg",
        "Heidenheim", "Hoffenheim", "Freiburg", "Augsburg", "Gladbach",
        "Stuttgart", "Bochum", "Dortmund", "Cologne", "Union",
        "Mainz", "Frankfurt", "Darmstadt"
    ]

    return render_template('teams.html', teams=teams)
@app.route('/team/<team_name>')
def team_detail(team_name):
    # conn = sqlite3.connect('my_database.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = """
    SELECT g.scorer_name, COUNT(*) AS goal_count
    FROM goals g
    JOIN teams t ON g.team_code = t.team_code
    WHERE t.team_name = ?
    GROUP BY g.scorer_name
    ORDER BY goal_count DESC
    LIMIT 1;
    """

    cursor.execute(query, (team_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        top_player = result[0]
        goals = result[1]
    else:
        top_player = "No data"
        goals = 0

    # return render_template('team_detail.html', team=team_name)
    return render_template('team_detail.html',
                               team=team_name,
                               player=top_player,
                               goals=goals)


if __name__ == '__main__':
# On PythonAnywhere, the 'Web' tab handles running the app,
    # but this allows for local testing if needed.
    app.run(debug=False)


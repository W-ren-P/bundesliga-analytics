import pandas as pd
from sqlalchemy import create_engine, inspect
import os

folder_path = '.'
os.chdir(folder_path)

csv_files = [
    'goals.csv',
    'match_cum_agg_stats.csv',
    'matches.csv',
    'referees.csv',
    'team_match_stats.csv',
    'teams.csv'
]

engine = create_engine('sqlite:///my_database.db')

print("--- Starting Import ---")
for file in csv_files:
    # Use the filename (without .csv) as the table name
    table_name = file.replace('.csv', '')

    try:
        df = pd.read_csv(file)
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Successfully imported: {table_name}")
    except Exception as e:
        print(f"Error importing {file}: {e}")

print("\n--- Final Table Stats ---")
inspector = inspect(engine)
tables = inspector.get_table_names()

for table in tables:
    count = pd.read_sql(f"SELECT COUNT(*) FROM {table}", engine).iloc[0, 0]
    print(f"Table: {table.ljust(20)} | Rows: {count}")

print("\nDatabase 'my_database.db' is ready for use.")

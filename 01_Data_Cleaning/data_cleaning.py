import os
import pandas as pd
from sqlalchemy import create_engine

# 1. Establish database connection (Update password if needed) with your MySQL username and password
DB_CONNECTION_URL = (
    'mysql+pymysql://<username>:<password>@localhost:3306/ipl_analytics'
)
engine = create_engine(DB_CONNECTION_URL)


def clean_ipl_data():
  print('Step 1: Extracting raw data from MySQL...')
  # Read the raw table into a Pandas DataFrame
  df = pd.read_sql('SELECT * FROM ipl_master', con=engine)
  print(f'Initial dataset shape: {df.shape}')

  print('Step 2: Performing data cleaning and type casting...')

  # Handle missing values for critical string columns (replace NaN with 'Unknown')
  string_columns = [
      'batter',
      'bowler',
      'venue',
      'match_won_by',
      'player_of_match',
  ]
  for col in string_columns:
    if col in df.columns:
      df[col] = df[col].fillna('Unknown').astype(str)

  # Handle missing values for numeric columns (replace NaN with 0)
  numeric_columns = [
      'runs_batter',
      'runs_extras',
      'runs_total',
      'wickets',
      'margin',
  ]
  for col in numeric_columns:
    if col in df.columns:
      df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

  # Convert specific columns to proper integers
  for col in ['runs_batter', 'runs_extras', 'runs_total']:
    if col in df.columns:
      df[col] = df[col].astype(int)

  # Optional: Drop duplicate rows if any exist
  initial_count = len(df)
  df = df.drop_duplicates()
  print(f'Removed {initial_count - len(df)} duplicate rows.')

  print('Step 3: Exporting cleaned data back to database & local CSV...')

  # Save cleaned dataset back to MySQL as a new clean table
  df.to_sql('ipl_cleaned_master', con=engine, if_exists='replace', index=False)

  # Save a backup copy locally inside the data cleaning folder
  output_dir = os.path.dirname(__file__)
  local_file_path = os.path.join(output_dir, 'ipl_cleaned_data.csv')
  df.to_csv(local_file_path, index=False)

  print(f'Data cleaning complete! Cleaned CSV saved to: {local_file_path}')
  print(f'Final cleaned dataset shape: {df.shape}')


if __name__ == '__main__':
  clean_ipl_data()
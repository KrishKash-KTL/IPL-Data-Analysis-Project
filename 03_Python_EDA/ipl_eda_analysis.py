import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

# 1. Establish database connection use your MySQL username and password
DB_CONNECTION_URL = (
    'mysql+pymysql://<username>:<password>@localhost:3306/ipl_analytics'
)
engine = create_engine(DB_CONNECTION_URL)

# 2. Setup output directory for generated plots
current_dir = os.path.dirname(__file__)
plots_dir = os.path.join(current_dir, 'generated_plots')
os.makedirs(plots_dir, exist_ok=True)


def run_eda_pipeline():
  print('Step 1: Extracting cleaned data from MySQL for EDA...')
  df = pd.read_sql('SELECT * FROM ipl_cleaned_master', con=engine)
  print(f'Dataset loaded successfully. Shape: {df.shape}')

  # Set plotting style
  sns.set_theme(style='whitegrid')

  # --- Plot 1: Top 10 Run-Scorers ---
  print('Generating Plot 1: Top Run-Scorers...')
  plt.figure(figsize=(12, 6))
  top_scorers = (
      df.groupby('batter')['runs_batter'].sum().reset_index()
  )  # type: ignore
  top_scorers = top_scorers.sort_values(
      by='runs_batter', ascending=False
  ).head(10)

  sns.barplot(
      data=top_scorers, x='runs_batter', y='batter', palette='viridis'
  )
  plt.title('Top 10 Run-Scorers in IPL Dataset', fontsize=14, fontweight='bold')
  plt.xlabel('Total Runs Scored', fontsize=12)
  plt.ylabel('Batter', fontsize=12)
  plt.tight_layout()
  plt.savefig(os.path.join(plots_dir, 'top_10_run_scorers.png'), dpi=300)
  plt.close()

  # --- Plot 2: Toss Decision Distribution ---
  print('Generating Plot 2: Toss Decision Distribution...')
  plt.figure(figsize=(8, 6))
  toss_counts = df['toss_decision'].value_counts()
  plt.pie(
      toss_counts,
      labels=toss_counts.index,
      autopct='%1.1f%%',
      startangle=140,
      colors=['#ff9999', '#66b3ff'],
  )
  plt.title(
      'Distribution of Toss Decisions (Bat vs Field)',
      fontsize=14,
      fontweight='bold',
  )
  plt.tight_layout()
  plt.savefig(os.path.join(plots_dir, 'toss_decision_distribution.png'), dpi=300)
  plt.close()

  # --- Plot 3: Top Venues by Match Count ---
  print('Generating Plot 3: Top Venues...')
  plt.figure(figsize=(12, 6))
  venue_counts = df[['match_id', 'venue']].drop_duplicates()
  top_venues = venue_counts['venue'].value_counts().head(10).reset_index()
  top_venues.columns = ['venue', 'match_count']

  sns.barplot(
      data=top_venues, x='match_count', y='venue', palette='crest'
  )
  plt.title('Top 10 Venues by Number of Matches', fontsize=14, fontweight='bold')
  plt.xlabel('Number of Matches', fontsize=12)
  plt.ylabel('Venue', fontsize=12)
  plt.tight_layout()
  plt.savefig(os.path.join(plots_dir, 'top_venues.png'), dpi=300)
  plt.close()

  print('EDA Complete! All visualization plots successfully saved inside:')
  print(f'-> {plots_dir}')


if __name__ == '__main__':
  run_eda_pipeline()
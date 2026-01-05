import pandas as pd
import os

data_dir = 'e:/ibrahim/Uni Courses/Techno/GlobalPath AI/data'
files = ['scholarships.xlsx', 'agents.xlsx', 'interview_prep.xlsx']

for file in files:
    path = os.path.join(data_dir, file)
    try:
        df = pd.read_excel(path)
        print(f"--- {file} ---")
        print(df.columns.tolist())
        # Print first row to see sample values for matching logic
        if not df.empty:
            print("Sample row:", df.iloc[0].to_dict())
    except Exception as e:
        print(f"Error reading {file}: {e}")

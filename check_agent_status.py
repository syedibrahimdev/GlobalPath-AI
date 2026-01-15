import pandas as pd
import os

data_dir = 'e:/ibrahim/Uni Courses/Techno/GlobalPath AI/data'
try:
    df = pd.read_excel(os.path.join(data_dir, 'agents.xlsx'))
    print(f"Unique Statuses: {df['Status'].unique()}")
except Exception as e:
    print(e)

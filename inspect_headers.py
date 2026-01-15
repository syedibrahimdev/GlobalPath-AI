import pandas as pd
import os

data_dir = 'e:/ibrahim/Uni Courses/Techno/GlobalPath AI/data'
files = ['recommendations.xlsx', 'applications.xlsx', 'faq_knowledgebase.xlsx', 'student_profiles.xlsx']

for file in files:
    path = os.path.join(data_dir, file)
    try:
        df = pd.read_excel(path)
        print(f"--- {file} ---")
        print(df.columns.tolist())
    except Exception as e:
        print(f"Error reading {file}: {e}")

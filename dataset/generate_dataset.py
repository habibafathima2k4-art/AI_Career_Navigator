import pandas as pd
import random

rows = []

careers = {
    "Software Developer": ["python", "java"],
    "Data Analyst": ["sql", "excel"],
    "Data Scientist": ["python", "statistics"],
    "UI Designer": ["design", "creativity"],
    "Digital Marketer": ["marketing", "communication"],
    "Business Analyst": ["excel", "communication"],
    "Cyber Security Analyst": ["networking"],
    "Cloud Engineer": ["cloud", "networking"],
    "DevOps Engineer": ["cloud", "python"],
    "Product Manager": ["communication", "management"],
    "QA Tester": ["testing"],
    "AI Engineer": ["python", "statistics"]
}

all_skills = [
    "python","java","sql","excel","communication","design",
    "marketing","statistics","networking","cloud"
]

interests = ["tech", "design", "business"]
education_levels = [0, 1]

for _ in range(200):

    career = random.choice(list(careers.keys()))
    base_skills = careers[career]

    row = {}

    for skill in all_skills:
        if skill in base_skills:
            row[skill] = 1
        else:
            row[skill] = 0
    
    career_interest_map = {
    "Software Developer": "tech",
    "Data Analyst": "tech",
    "Data Scientist": "tech",
    "Cyber Security Analyst": "tech",
    "Cloud Engineer": "tech",
    "DevOps Engineer": "tech",
    "AI Engineer": "tech",
    "QA Tester": "tech",

    "UI Designer": "design",

    "Digital Marketer": "business",
    "Business Analyst": "business",
    "Product Manager": "business"
}
    row["interest"] = career_interest_map[career]
    row["education"] = random.choice(education_levels)
    row["career"] = career

    rows.append(row)

df = pd.DataFrame(rows)

df.to_csv("career_data.csv", index=False)

print("Dataset generated successfully with", len(df), "rows")

from flask import Flask, render_template, request
from database import get_connection
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('model/model.pkl', 'rb'))

career_info = {
    "Software Developer": {
        "salary": "₹4–12 LPA",
        "skills": ["python", "java"],
        "description": "Develops software applications."
    },
    "Data Analyst": {
        "salary": "₹3–10 LPA",
        "skills": ["sql", "excel"],
        "description": "Analyzes data."
    },
    "Data Scientist": {
        "salary": "₹6–20 LPA",
        "skills": ["python", "statistics"],
        "description": "Builds ML models."
    },
    "UI Designer": {
        "salary": "₹3–8 LPA",
        "skills": ["design", "communication"],
        "description": "Designs UI."
    },
    "Digital Marketer": {
        "salary": "₹3–10 LPA",
        "skills": ["marketing", "communication"],
        "description": "Promotes products."
    },
    "Cyber Security Analyst": {
        "salary": "₹6–18 LPA",
        "skills": ["networking"],
        "description": "Handles security."
    },
    "Cloud Engineer": {
        "salary": "₹6–18 LPA",
        "skills": ["cloud", "networking"],
        "description": "Manages cloud."
    },
    "DevOps Engineer": {
        "salary": "₹7–20 LPA",
        "skills": ["cloud", "python"],
        "description": "Deployment automation."
    },
    "Product Manager": {
        "salary": "₹8–25 LPA",
        "skills": ["communication"],
        "description": "Manages product."
    },
    "QA Tester": {
        "salary": "₹3–8 LPA",
        "skills": ["testing"],
        "description": "Tests software."
    },
    "AI Engineer": {
        "salary": "₹10–30 LPA",
        "skills": ["python", "statistics"],
        "description": "Builds AI."
    },
    "Not Sure - Improve Skills": {
        "salary": "N/A",
        "skills": [],
        "description": "Improve your skills."
    }
}


def preprocess_input(user_skills, interest, education):
    skills_master = [
        'python','java','sql','excel','communication','design',
        'marketing','statistics','networking','cloud'
    ]

    vector = []

    for skill in skills_master:
        vector.append(1 if skill in user_skills else 0)

    interest_map = {'tech':0, 'design':1, 'business':2}
    education_map = {'ug':0, 'pg':1}

    return vector + [
        interest_map.get(interest.lower(), 0),
        education_map.get(education.lower(), 0)
    ]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    skills = request.form.getlist('skills')
    interest = request.form['interest']
    education = request.form['education']

    data = preprocess_input(skills, interest, education)

    data_df = pd.DataFrame([data], columns=[
        'python','java','sql','excel','communication','design',
        'marketing','statistics','networking','cloud','interest','education'
    ])

    prediction = model.predict(data_df)
    career = prediction[0]

    probs = model.predict_proba(data_df)[0]
    labels = model.classes_
    career_probs = list(zip(labels,probs))
    career_probs.sort(key=lambda x: x[1], reverse=True)

    top_careers=career_probs[:3]
    chart_labels = [c[0] for c in top_careers]
    chart_values = [round(c[1]*100, 2) for c in top_careers]
    confidence = round(max(probs) * 100, 2)

    if confidence < 15:
        career = "Not Sure - Improve Skills"

    details = career_info.get(career, {})

    required_skills = details.get("skills", [])
    matched = len(set(required_skills) & set(skills))

    match_percent = int((matched / len(required_skills)) * 100) if required_skills else 0

    if career == "Not Sure - Improve Skills":
        match_percent = 0

    if required_skills:
        missing_skills = list(set(required_skills) - set(skills))
    else:
        missing_skills = []

    if missing_skills:
        suggestions = [f"Learn {s}" for s in missing_skills]
    else:
        suggestions = ["Build projects", "Practice skills"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions (skills, interest, education, prediction, match_score)
    VALUES (%s, %s, %s, %s, %s)
    """, (
        ",".join(skills),
        interest,
        education,
        career,
        match_percent
    ))

    conn.commit()
    conn.close()

    return render_template(
        'result.html',
        prediction=career,
        salary=details.get("salary", "N/A"),
        skills=required_skills,
        description=details.get("description", ""),
        match=match_percent,
        confidence=confidence,
        missing_skills=missing_skills,
        suggestions=suggestions,
        chart_labels=chart_labels,
        chart_values=chart_values,
        explanation=""
    )


@app.route('/admin')
def admin():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    data = cursor.fetchall()

    conn.close()

    return render_template('admin.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
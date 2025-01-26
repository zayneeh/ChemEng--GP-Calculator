import streamlit as st
import pandas as pd

# Load curriculum data from CSV
@st.cache
def load_curriculum():
    return pd.read_csv('curriculum.csv')

curriculum = load_curriculum()

# Dictionary for converting letter grades to points
grade_points = {
    'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0
}

def calculate_gpa(grades, credits):
    if not grades or not credits:
        return 0
    total_points = sum(grade * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return total_points / total_credits if total_credits else 0

st.title('Chemical Engineering GPA Calculator')

# Select level and semester
part = st.selectbox('Select your level:', curriculum['Part'].unique())
semester = st.selectbox('Select your semester:', curriculum['Semester'].unique())

# Filter the curriculum based on selected level and semester
filtered_curriculum = curriculum[(curriculum['Part'] == part) & (curriculum['Semester'] == semester)]

if not filtered_curriculum.empty:
    grades = {}
    for index, row in filtered_curriculum.iterrows():
        grade = st.text_input(f"Enter grade for {row['Course']} ({row['Credits']} credits):", key=f"grade_{index}")
        if grade:
            grades[row['Course']] = (grade, row['Credits'])

    if st.button('Calculate My GPA'):
        valid_grades = [grade_points.get(grade[0].upper(), 0) for grade in grades.values() if grade[0].upper() in grade_points]
        credits = [float(grade[1]) for grade in grades.values() if grade[0].upper() in grade_points]
        if valid_grades and credits:
            gpa = calculate_gpa(valid_grades, credits)
            st.success(f'Your GPA is {gpa:.2f}')
        else:
            st.error("Please enter valid grades for at least one course.")
else:
    st.write("No courses available for the selected level and semester.")

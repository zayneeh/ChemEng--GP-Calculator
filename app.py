import streamlit as st
import pandas as pd

# Load curriculum data from CSV
@ st.cache_data 
def load_curriculum():
    return pd.read_csv('curriculum.csv')

curriculum = load_curriculum()

# Dictionary for converting letter grades to points
grade_points = {
    'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0
}

def grade_to_points(grades):
    points = []
    for grade in grades:
        if grade.strip().isdigit():  # handling numeric grades input
            grade = int(grade)
            if grade >= 70:
                points.append(5.0)
            elif grade >= 60:
                points.append(4.0)
            elif grade >= 50:
                points.append(3.0)
            elif grade >= 45:
                points.append(2.0)
            elif grade >= 40:
                points.append(1.0)
            else:
                points.append(0.0)
        else:  # handling letter grades input
            points.append(grade_points.get(grade.strip().upper(), 0))
    return points

def calculate_gpa(grades, credits):
    if not grades or not credits:
        return 0
    total_points = sum(grade * unit for grade, unit in zip(grades, units))
    total_units = sum(units)
    return total_points / total_units if total_units else 0

st.title('Chemical Engineering GPA Calculator')

# Select level and semester
part = st.selectbox('Select your level:', curriculum['Part'].unique())
semester = st.selectbox('Select your semester:', curriculum['Semester'].unique())

# Filter the curriculum based on selected level and semester
filtered_curriculum = curriculum[(curriculum['Part'] == part) & (curriculum['Semester'] == semester)]

if not filtered_curriculum.empty:
    grades = {}
    for index, row in filtered_curriculum.iterrows():
        grade = st.text_input(f"Enter grade for {row['Course']} ({row['Unit']} units):", key=f"grade_{index}")
        if grade:
            grades[row['Course']] = (grade, row['Units'])

    if st.button('Calculate My GPA'):
        # Extract grades and credits from dictionary
        grades_input = [grade[0] for grade in grades.values()]
        units = [float(grade[1]) for grade in grades.values()]
        # Convert grades to points
        valid_grades = grade_to_points(grades_input)
        # Calculate GPA
        if valid_grades and units:
            gpa = calculate_gpa(valid_grades, units)
            st.success(f'Your GPA is {gpa:.2f}')
        else:
            st.error("Please enter valid grades for at least one course.")
else:
    st.write("No courses available for the selected level and semester.")

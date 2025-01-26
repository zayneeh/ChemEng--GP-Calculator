import streamlit as st
import pandas as pd

# Load curriculum data from CSV
@st.cache_data 
def load_curriculum():
    return pd.read_csv('curriculum.csv')

curriculum = load_curriculum()

# Dictionary for converting letter grades to points
grade_points = {
    'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0
}

# Function to handle both numeric and letter grades input
def grade_to_points(grade):
    if grade.isdigit():  # Handle numeric grades input
        grade = int(grade)
        if grade >= 70:
            return 5.0
        elif grade >= 60:
            return 4.0
        elif grade >= 50:
            return 3.0
        elif grade >= 45:
            return 2.0
        elif grade >= 40:
            return 1.0
        else:
            return 0.0
    else:  # Handle letter grades input
        return grade_points.get(grade.upper(), 0)

# Function to calculate GPA based on grades and units
def calculate_gpa(grades, units):
    if not grades or not units:
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
    grades = []
    units = []
    for index, row in filtered_curriculum.iterrows():
        grade_input = st.text_input(f"Enter grade for {row['Course']} ({row['Units']} units):", key=f"grade_{index}")
        if grade_input:  # Collect only non-empty inputs
            grade_point = grade_to_points(grade_input)
            if grade_point is not None:  # Ensure valid grade conversion
                grades.append(grade_point)
                units.append(float(row['Units']))

    if st.button('Calculate My GPA'):
        if grades and units:
            gpa = calculate_gpa(grades, units)
            st.success(f'Your GPA is {gpa:.2f}')
        else:
            st.error("Please enter valid grades for at least one course.")
else:
    st.write("No courses available for the selected level and semester.")

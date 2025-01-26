import streamlit as st
import pandas as pd 

# Dictionary for converting letter grades to points
grade_points = {
    'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0,
    # Assuming 'A' grade range from 70 to 100 for numeric input
    '70-100': 5.0, '60-69': 4.0, '50-59': 3.0, '45-49': 2.0, '40-44': 1.0, '0-39': 0.0
}

# Load curriculum data from CSV
@st.cache
def load_curriculum():
    return pd.read_csv('curriculum.csv')

curriculum = load_curriculum()

def calculate_gpa(grades, credits):
    total_points = sum(grade * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return total_points / total_credits if total_credits else 0

# Get unique levels and semesters from the dataset
levels = curriculum['Level'].unique()
semesters = curriculum['Semester'].unique()

st.title('Chemical Engineering GPA Calculator')

level = st.selectbox('Select your level:', levels)
semester = st.selectbox('Select your semester:', semesters)

# Filter the curriculum based on selected level and semester
filtered_curriculum = curriculum[(curriculum['Level'] == level) & (curriculum['Semester'] == semester)]

# Show courses and ask for grades
if not filtered_curriculum.empty:
    for index, row in filtered_curriculum.iterrows():
        st.write(f"{row['Course']} - {row['Credits']} credits")
    grades_input = st.text_input('Enter your grades for the courses listed (comma-separated, e.g., A, B, C):').upper().split(',')
    # Convert grades to points, calculate GPA, etc.

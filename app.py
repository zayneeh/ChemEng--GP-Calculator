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

def calculate_gpa(grades, credits):
    total_points = sum(grade * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return total_points / total_credits if total_credits else 0

st.title('Chemical Engineering GPA Calculator')

# User selects level and semester
level = st.selectbox('Select your level:', options=['Part 1', 'Part 2', 'Part 3', 'Part 4', 'Part 5'])
semester = st.selectbox('Select your semester:', options=['Semester 1', 'Semester 2'])

curriculum = load_curriculum()
courses = curriculum[Part][Semester]
course_names, course_credits = zip(*courses)

# User selects grade input type
grade_input_type = st.radio("Select your grade input type:", ('Letters', 'Numbers'))

# Input grades based on selected type
if grade_input_type == 'Letters':
    grades_input = st.text_input('Enter your grades separated by commas (e.g., A, B, C):').upper().split(',')
else:
    grades_input = st.text_input('Enter your grades as numbers separated by commas (e.g., 75, 88, 92):').split(',')
    # Convert numeric grades to letter grades based on the scale defined
    grades_input = [next(k for k, v in grade_points.items() if int(num) in range(int(k.split('-')[0]), int(k.split('-')[1]) + 1)) for num in grades_input]

# Convert letter grades to grade points
try:
    grades = [grade_points[grade.strip()] for grade in grades_input if grade.strip() in grade_points]
    credits = [float(credit) for credit in course_credits]
except ValueError:
    st.error("Please check your input. Grades should be valid letters (A-F) or numbers (0-100).")
    st.stop()

# Calculate GPA
if st.button('Calculate My GPA'):
    if len(grades) == len(credits):
        gpa = calculate_gpa(grades, credits)
        st.success(f'Your GPA is {gpa:.2f}')
    else:
        st.error("The number of grades entered does not match the number of courses. Please check your input.")

st.sidebar.info("This tool allows you to calculate your GPA using either letter grades or numerical scores. Choose your preferred method and enter your grades to see your GPA.")

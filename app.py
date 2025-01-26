import streamlit as st
import pandas as pd

# Dictionary for converting letter grades to points
grade_points = {
    'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0
}

def grade_to_points(grades):
    points = []
    for grade in grades:
        if grade.isdigit():  # handling numeric grades input
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
            points.append(grade_points.get(grade, 0))
    return points

@st.cache
def load_curriculum():
    return pd.read_csv('curriculum.csv')

curriculum = load_curriculum()

def calculate_gpa(grades, credits):
    total_points = sum(grade * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return total_points / total_credits if total_credits else 0

levels = curriculum['Level'].unique()
semesters = curriculum['Semester'].unique()

st.title('Chemical Engineering GPA Calculator')

level = st.selectbox('Select your level:', levels)
semester = st.selectbox('Select your semester:', semesters)

filtered_curriculum = curriculum[(curriculum['Level'] == level) & (curriculum['Semester'] == semester)]

if not filtered_curriculum.empty:
    for index, row in filtered_curriculum.iterrows():
        st.write(f"{row['Course']} - {row['Credits']} credits")
    grades_input = st.text_input('Enter your grades for the courses listed (comma-separated, e.g., A, B, C or 85, 70, 92):').upper().split(',')
    grades_input = [grade.strip() for grade in grades_input]
    grades_points = grade_to_points(grades_input)
    credits = [float(credit) for credit in filtered_curriculum['Credits']]
    
    if st.button('Calculate My GPA'):
        if len(grades_points) == len(credits):
            gpa = calculate_gpa(grades_points, credits)
            st.success(f'Your GPA is {gpa:.2f}')
        else:
            st.error("The number of grades entered does not match the number of courses. Please check your input.")

from django.shortcuts import render
from .forms import QuestionForm
import pandas as pd
import re

df = pd.read_csv('C:/Users/chand/OneDrive/Desktop/LMS_Portal/qa/students.csv')

def parse_question(question):
    question = question.lower()
    response = "Sorry, I couldn't understand the question."

    id_match = re.search(r'(\d{4})', question)
    if not id_match:
        return "Please specify a student ID like 1001."

    student_id = int(id_match.group(1))
    student = df[df['id'] == student_id]

    if student.empty:
        return f"No student found with ID {student_id}."

    student = student.iloc[0]

    if "info" in question or "details" in question:
        response = (
            f"ID: {student.id}\n"
            f"Name: {student.name}\n"
            f"Class: {student['class']}\n"
            f"Email: {student.email}\n"
        )
    elif "math" in question:
        response = f"{student.name}'s Maths marks: {student.maths}"
    elif "science" in question:
        response = f"{student.name}'s Science marks: {student.science}"
    elif "social" in question:
        response = f"{student.name}'s Social marks: {student.social}"
    elif "email" in question:
        response = f"{student.name}'s Email: {student.email}"

    return response

def qa_view(request):
    answer = None
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = parse_question(question)
    else:
        form = QuestionForm()

    return render(request, 'qa/index.html', {'form': form, 'answer': answer})

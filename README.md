# 📘 Simple Django LMS CSV Q&A Portal – Step-by-Step Guide

This project is a basic **Q&A Portal** built using **Django** that reads **student data from a CSV file** and answers simple queries like:
- “Need info about 1001?”
- “Marks for social subject 1001?”
- “What is the email of student 1002?”

---

## 📁 Folder Structure

```
lms_csv_project/
├── manage.py
├── students.csv
├── lms_csv_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── qa/
│   ├── __init__.py
│   ├── forms.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── qa/
│           └── index.html
```

---

## 📝 Step-by-Step Setup

### 1. Install Django & pandas

```bash
pip install django pandas
```

---

### 2. Create Django Project

```bash
django-admin startproject lms_csv_project
cd lms_csv_project
```

---

### 3. Create App

```bash
python manage.py startapp qa
```

Add `qa` to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'qa',
]
```

---

### 4. Add `students.csv` to Project Root

```csv
id,name,class,maths,science,social,email
1001,Amit Sharma,10,85,92,78,amit@example.com
1002,Neha Verma,10,75,89,82,neha@example.com
1003,Ravi Kumar,9,65,72,70,ravi@example.com
```

---

### 5. `qa/forms.py`

```python
from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(label='Ask a question', max_length=200)
```

---

### 6. `qa/views.py`

```python
from django.shortcuts import render
from .forms import QuestionForm
import pandas as pd
import re

df = pd.read_csv('students.csv')

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
```

---

### 7. `qa/urls.py`

```python
from django.urls import path
from .views import qa_view

urlpatterns = [
    path('', qa_view, name='qa_view'),
]
```

---

### 8. `lms_csv_project/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('qa.urls')),
]
```

---

### 9. Template: `qa/templates/qa/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Student Info Q&A</title>
</head>
<body>
    <h2>Ask Your Question (e.g. "Need info about 1001")</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Ask</button>
    </form>

    {% if answer %}
        <h3>Answer:</h3>
        <pre>{{ answer }}</pre>
    {% endif %}
</body>
</html>
```

---

### 10. Run the Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) and try questions like:
- `Need info about 1001`
- `Marks for science subject 1002`
- `What is the email for 1003`

---

## ✅ Sample Output

> **Question**: Marks for science 1001  
> **Answer**: Amit Sharma's Science marks: 92

> **Question**: Need info about 1002  
> **Answer**:  
> ID: 1002  
> Name: Neha Verma  
> Class: 10  
> Email: neha@example.com

---

## 🔧 Tips

- Make sure `students.csv` is in the same folder where you run the server.
- Always use `from .forms import QuestionForm` in `views.py` (relative import).
- You can extend this system to handle more subjects, error checking, and CSV uploads.

---

Happy Coding! 🚀

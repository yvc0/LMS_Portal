from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(label='Ask a question', max_length=200)

from django.urls import path
from qa.views import qa_view

urlpatterns = [
    path('', qa_view, name='qa_view'),
]
from django.urls import path
from .quiz.views import *

from .add_questions.views import *


urlpatterns = [
    path('POSTQuiz/', POSTQuiz.as_view()),
    path('PUTQuiz/<slug:id>/', PUTQuiz.as_view()),
    path('GETAllQuiz/', GETAllQuiz.as_view()),
    path('GETQuizCount/', GETQuizCount.as_view()),

    path('POSTQuestions/', POSTQuestions.as_view()),
]


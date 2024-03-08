from django.urls import path
from .quiz.views import *

from .add_questions.views import *
from .enroll_and_result.views import POSTQuizEnrollment

urlpatterns = [
    path('POSTQuiz/', POSTQuiz.as_view()),
    path('PUTQuiz/<slug:id>/', PUTQuiz.as_view()),
    path('GETAllQuiz/', GETAllQuiz.as_view()),
    path('GETQuizCount/', GETQuizCount.as_view()),

    path('POSTQuestions/', POSTQuestions.as_view()),
    path('GETAllQuestionsByQuizId/<slug:quizId>/', GETAllQuestionsByQuizId.as_view()),
    path('PUTQuestionById/<slug:questionId>/', PUTQuestionById.as_view()),
    path('PUTOption/<slug:optionId>/', PUTOption.as_view()),
    path('POSTOption/', POSTOption.as_view()),
    path('POSTQuizEnrollment/', POSTQuizEnrollment.as_view())
]




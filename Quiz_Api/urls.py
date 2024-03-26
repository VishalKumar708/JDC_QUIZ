from django.urls import path
from .quiz.views import *

from .add_questions.views import *
from .enroll_and_result.views import *
from .quiz_play.views import *

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
    path('POSTQuizEnrollment/', POSTQuizEnrollment.as_view()),
    path('GETAllQuizResult/', GETAllQuizEnrollment.as_view()),
    path('GETAllQuestionsByQuizIdAndUserId/<slug:userId>/<slug:quizId>/', GETAllQuestionsByUserIdAndQuizId.as_view()),

    path('POSTQuizPlay/', POSTQuizPlay.as_view()),
    # path('GETReadyToPlayQuiz/<slug:userId>/<slug:quizId>/', GETReadyPlayQuiz.as_view())

]




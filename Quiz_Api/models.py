from django.db import models
from utils.base_model import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    isVerified = models.BooleanField(default=False)


class Quiz(BaseModel):
    title = models.CharField(max_length=250)
    startDate = models.DateField()
    endDate = models.DateField()
    resultDate = models.DateField()
    prize = models.CharField(max_length=150)
    duration = models.CharField(max_length=50)
    # totalQuestions = models.IntegerField(default=None, null=True)
    order = models.IntegerField()
    organization_id = models.ForeignKey('Quiz_Api.Organization', on_delete=models.SET_NULL,
                                     related_name="organization_quiz", null=True, default=None, blank=True)
    isVerified = models.BooleanField(default=False)


class QuizQuestions(BaseModel):
    TYPE_CHOICES = [
        ("radio", "Radio"),
        ("checkbox", "Checkbox")
    ]
    LEVEL_CHOICE = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard")
    ]

    quiz_id = models.ForeignKey('Quiz_Api.Quiz', on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.TextField()
    type = models.CharField(max_length=150, choices=TYPE_CHOICES)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICE)
    # isVerified = models.BooleanField(default=True)


class QuizOptions(BaseModel):
    question_id = models.ForeignKey('Quiz_Api.QuizQuestions', on_delete=models.CASCADE, related_name='options')
    option = models.TextField()
    correctOption = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)
    # isVerified = models.BooleanField(default=True)


class QuizEnrollment(BaseModel):
    STATUS_CHOICES = (
        ('enroll', "Enroll"),
        ('start', "Start"),
        ('playing', "Playing"),
        ('complete', "Complete"),
    )
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='quiz_enrollments')
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='enrollments')
    enrollmentDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    playedDate = models.DateTimeField(null=True, blank=True)
    # score = models.IntegerField(default=0)
    timeTaken = models.IntegerField(default=0)
    correctAnswer = models.IntegerField(default=0)
    incorrectAnswer = models.IntegerField(default=0)
    pendingAnswer = models.IntegerField(default=0)
# Create your models here.


class QuizPlay(BaseModel):
    userId = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='quiz_plays')
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_plays')
    questionId = models.ForeignKey('Quiz_Api.QuizQuestions', on_delete=models.CASCADE, related_name='quiz_plays')
    answerId = models.ForeignKey('Quiz_Api.QuizOptions', on_delete=models.CASCADE, related_name='quiz_plays')


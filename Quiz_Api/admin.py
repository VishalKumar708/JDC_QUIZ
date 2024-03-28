from django.contrib import admin
from .models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Organization, OrganizationAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "startDate", "endDate", "resultDate", "prize", "duration",
                    "organization_id", "order", "isActive", "isVerified"]
    # list_max_show_all = 100000000


admin.site.register(Quiz, QuizAdmin)


class QuizQuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "quiz_id", "question", "type", "level", "isActive"]


admin.site.register(QuizQuestions, QuizQuestionsAdmin)


class QuizAnswersAdmin(admin.ModelAdmin):
    list_display = ["id", "question_id", "option", "correctOption", "isActive"]


admin.site.register(QuizOptions, QuizAnswersAdmin)


class QuizEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'quiz_id', 'enrollmentDate', 'status', 'playedDate', 'score', 'timeTaken',
                     'correctAnswer', 'incorrectAnswer', 'pendingAnswer']


admin.site.register(QuizEnrollment, QuizEnrollmentAdmin)
# Register your models here.


class QuizPlayAdmin(admin.ModelAdmin):
    list_display = ["id", "userId", "quizId", "questionId", "answerId"]


admin.site.register(QuizPlay, QuizPlayAdmin)



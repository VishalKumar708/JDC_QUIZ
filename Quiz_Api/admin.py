from django.contrib import admin
from .models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Organization, OrganizationAdmin)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "startDate", "endDate", "resultDate", "prize", "duration",
                    "organization_id", "order", "isActive", "isVerified"]
    # list_max_show_all = 100000000
    list_filter = ['startDate', 'endDate', 'resultDate', 'isActive', 'isVerified']
    search_fields = ['title']

# admin.site.register(Quiz, QuizAdmin)

@admin.register(QuizQuestions)
class QuizQuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "quiz_id", "question", "type", "level", "isActive"]
    list_filter = ['quiz_id', "type", "level", "isActive"]


# admin.site.register(QuizQuestions, QuizQuestionsAdmin)

@admin.register(QuizOptions)
class QuizAnswersAdmin(admin.ModelAdmin):
    list_display = ["id", "question_id", "option", "correctOption", "isActive"]
    list_filter = ['question_id', "isActive", "correctOption"]

# admin.site.register(QuizOptions, QuizAnswersAdmin)

@admin.register(QuizEnrollment)
class QuizEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'quiz_id', 'enrollmentDate', 'status', 'playedDate', 'timeTaken',
                     'correctAnswer', 'incorrectAnswer', 'pendingAnswer']
    list_filter = ['user_id', 'quiz_id', 'correctAnswer', 'incorrectAnswer', 'pendingAnswer']

# admin.site.register(QuizEnrollment, QuizEnrollmentAdmin)
# Register your models here.


@admin.register(QuizPlay)
class QuizPlayAdmin(admin.ModelAdmin):
    list_display = ["id", "userId", "quizId", "questionId", "answerId"]
    list_filter = ['userId', 'quizId', 'questionId']

# admin.site.register(QuizPlay, QuizPlayAdmin)



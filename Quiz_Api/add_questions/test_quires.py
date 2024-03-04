from ..models import QuizQuestions, QuizOptions
from django.db.models import Subquery, OuterRef


def function(a=None, b=None):
    quiz_questions = QuizQuestions.objects.prefetch_related(
        'options'
    ).filter(quiz_id=1)

    if b is not None:
        quiz_questions = quiz_questions.filter(isActive=b)
        # quiz_questions = quiz_questions.filter
        print('question_queryset=> ', quiz_questions)
    if a is not None:
        quiz_questions = quiz_questions.filter(
            options__in=Subquery(
                QuizOptions.objects.exclude(
                    question_id=OuterRef('pk'),  # Assuming 'question_id' is the correct field name
                    isActive= not a
                ).value('id')  # Assuming 'id' is the correct primary key field name
            )
        )
        print('answer queryset=> ', quiz_questions)
    # Now you can access the related answers for each quiz question
    for question in quiz_questions:
        print("Question:", question.question)
        # print("Type:", question.type)
        # print("Level:", question.level)
        print("isActive: ", question.isActive)
        for answer in question.options.all():
            print("id: ", answer.id)
            print("- Option:", answer.option)
            # print("  Correct Option:", answer.correctOption)
            print("isActive: ", answer.isActive)
        print("---------------------------------")

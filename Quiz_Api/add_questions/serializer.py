from rest_framework import serializers
from ..models import Quiz, QuizQuestions, QuizAnswers
from django.db import transaction


class QuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
    type = serializers.ChoiceField(choices=["radio", "checkbox"])
    level = serializers.CharField()


class CreateQuestionSerializer(serializers.Serializer):
    quizId = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
    question = QuestionSerializer()
    options = serializers.ListField(child=serializers.CharField())
    correct_answer = serializers.ListField(child=serializers.IntegerField())


    def create(self, validated_data):

        # Extract data from validated_data
        quiz_id = validated_data['quizId']
        question_data = validated_data['question']
        options_data = validated_data['options']
        correct_answers = validated_data['correct_answer']

        # List to store created question instances
        question_instance = None

        # database transaction
        with (transaction.atomic()):
            try:
                # 1st step: Create QuizQuestions instance
                question_instance = QuizQuestions.objects.create(
                    quiz_id=quiz_id,
                    question=question_data['text'],
                    type=question_data['type'],
                    level=question_data['level']
                )
                # question_instances.append(question_instance.id)
                # 2 Step: match correct answer value
                options = []
                total_options = len(options_data)

                for i in range(total_options):
                    # match correct option to given options
                    if i in correct_answers:
                        options.append(
                            QuizAnswers(quizQuestion_id=question_instance, option=options_data[i], correctOption=True))
                    else:
                        options.append(QuizAnswers(quizQuestion_id=question_instance, option=options_data[i]))

                # step3: create bulk answers
                QuizAnswers.objects.bulk_create(options)

            except Exception:
                # Rollback transaction for the current question if any error occurs
                transaction.set_rollback(True)

        return question_instance





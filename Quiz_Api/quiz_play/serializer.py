from ..models import QuizPlay, QuizEnrollment, QuizOptions
from rest_framework import serializers
from collections import Counter
from django.utils import timezone


class CreateQuizPlaySerializer(serializers.ModelSerializer):
    optionId = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=QuizOptions.objects.all()))
    quizStatus = serializers.ChoiceField(choices=[choice for choice in QuizEnrollment.STATUS_CHOICES if choice[0] in ['playing', 'complete']], source='status')

    class Meta:
        model = QuizPlay
        fields = ["userId", "quizId", "questionId", "optionId", "quizStatus"]

    def to_internal_value(self, data):
        errors = {}
        validated_data = None
        optionId = data.get('optionId')

        # default validation
        try:
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()
            for key, value in new_errors.items():
                errors[key] = value

        if optionId:
            try:
                user_answers = set(optionId)
                if type(optionId) is list and len(optionId) != len(user_answers):
                    errors['optionId'] = ['Cannot pass the same value more than once.']
            except TypeError:
                pass
        if errors:
            raise serializers.ValidationError(errors)
        return validated_data

    def validate(self, attrs):
        # print("attrs==> ", attrs)
        user_instance = attrs.get('userId')
        quiz_instance = attrs.get("quizId")
        question_instance = attrs.get('questionId')
        answers_objects = attrs.get('optionId')

        errors = {}
        if user_instance and quiz_instance:
            enrolled_objects = QuizEnrollment.objects.filter(user_id=user_instance, quiz_id=quiz_instance)
            if not enrolled_objects.exists():
                errors['userId'] = [f"You are not enrolled in this quiz, Please first enrolled in the quiz."]
            elif enrolled_objects[0].status == 'complete':
                print("quiz__status=> ", enrolled_objects[0].status)
                raise serializers.ValidationError({'userId': 'You have finished this quiz.'})
        if quiz_instance and question_instance:
            if quiz_instance != question_instance.quiz_id:
                errors['questionId'] = [f"Invalid Question for this quiz."]

        if answers_objects and quiz_instance:
            invalid_options = {answer.id: ["Invalid Option."] for answer in answers_objects if answer.question_id != question_instance}
            if invalid_options:
                errors['optionId'] = invalid_options

        if user_instance and quiz_instance and question_instance:
            filtered_data = QuizPlay.objects.filter(quizId=quiz_instance, questionId=question_instance, userId=user_instance).count()
            if filtered_data > 0:
                errors["userId"] = ["You have already attempt this question."]

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        options_instance = validated_data.get("optionId")
        user_instance = validated_data.get('userId')
        quiz_instance = validated_data.get('quizId')
        question_instance = validated_data.get('questionId')
        correct_options = question_instance.options.filter(correctOption=True)
        quiz_status = validated_data.get('status')
        # print("quiz_status=> ", quiz_status)

        # store user answers
        objects = [QuizPlay(userId=user_instance, quizId=quiz_instance, questionId=question_instance, answerId=option) for option in options_instance]
        # print("objects==> ", objects)
        created_options_instances = QuizPlay.objects.bulk_create(objects)

        # match user answer is correct or not
        enrollment_user_instance = QuizEnrollment.objects.filter(user_id=user_instance, quiz_id=quiz_instance).first()
        if Counter(correct_options) == Counter(options_instance):
            enrollment_user_instance.correctAnswer = enrollment_user_instance.correctAnswer+1
            # print("total correct answer==> ", enrollment_user_instance.correctAnswer)
        else:
            enrollment_user_instance.incorrectAnswer = enrollment_user_instance.incorrectAnswer+1
            # print("total incorrect answers ==> ", enrollment_user_instance.incorrectAnswer)
        enrollment_user_instance.playedDate = timezone.now()
        print("enrollment_user=>", enrollment_user_instance.playedDate)
        enrollment_user_instance.status = quiz_status
        enrollment_user_instance.save()

        return created_options_instances



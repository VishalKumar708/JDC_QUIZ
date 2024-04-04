
from rest_framework import serializers
from ...models import Quiz, QuizQuestions, QuizOptions
from django.db import transaction
from collections import Counter
from utils.validators import compare_dates
from django.conf import settings

datetime_format = getattr(settings, 'DEFAULT_DATE_FORMAT', "%d/%m/%Y")


class QuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
    type = serializers.ChoiceField(choices=["radio", "checkbox"])
    level = serializers.CharField()


class OptionsSerializer(serializers.ModelSerializer):
    correctOption = serializers.BooleanField(required=True)

    class Meta:
        model = QuizOptions
        fields = ["option", "isActive", "correctOption", "order"]


class CreateQuestionSerializer(serializers.Serializer):
    quizId = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
    question = QuestionSerializer()
    options = serializers.ListField(child=OptionsSerializer())
    # correct_answer = serializers.ListField(child=serializers.IntegerField())

    def to_internal_value(self, data):
        # print("data==> ", data)
        errors = {}
        if data:
            quiz_id = data.get('quizId')
            question_data = data.get('question')
            options_data = data.get('options')

            # check quiz.startDate > today date or not
            try:
                quiz_instance = Quiz.objects.get(id=quiz_id)
                quiz_startDate_greate_then_todayDate = compare_dates(
                    end_date=quiz_instance.startDate.strftime(datetime_format))
                quiz_endDate_greater_then_todayDate = compare_dates(
                    end_date=quiz_instance.endDate.strftime(datetime_format))

                print("quiz.startDate==> ", quiz_startDate_greate_then_todayDate)
                print("quiz.endDate==> ", quiz_endDate_greater_then_todayDate)

                if quiz_startDate_greate_then_todayDate and quiz_endDate_greater_then_todayDate:
                    raise serializers.ValidationError({
                        'quiz_id': ["Quiz has ended now you can't add more questions."]
                    })
                elif quiz_startDate_greate_then_todayDate:
                    raise serializers.ValidationError({
                        'quiz_id': ["Quiz has started now you can't add more questions."]
                    })
            except Quiz.DoesNotExist:
                # print('error in quiz instance serializer')
                pass
            except ValueError:
                # print('error in quiz instance serializer')
                pass

            # check same option shouldn't come more than 1 time
            correct_answers_count = 0 if options_data is None else sum(1 for item in options_data if item.get('correctOption') == True)
            print("correct_answers_count==> ", correct_answers_count)
            option_counts = Counter(option['option'].strip().lower() for option in options_data if option['option'] is not None)
            # Find the key with the maximum integer value
            max_key = max(option_counts, key=option_counts.get)
            if option_counts[max_key] > 1:
                errors["options"] = [f"'{max_key}' option came {option_counts[max_key]} times."]
            # print('correct_answer_count==> ', correct_answers_count)
            # custom validation

            # check a question exist only one time in a quiz
            if quiz_id and question_data.get('text'):
                print("condition working..")
                filtered_data = QuizQuestions.objects.filter(quiz_id=quiz_id, question__iexact=question_data['text'].strip()).count()
                if filtered_data > 0:
                    errors['question'] = {'text': ["This question is already Added."]}

            # apply validation to add correct_answers based on question 'type'
            # if user select question 'type' =='checkbox' then he must enter at least two correct options
            if correct_answers_count and correct_answers_count > 0:
                if question_data.get('type') == 'checkbox':
                    if correct_answers_count < 2:
                        errors['options'] = [f"Please select more then one 'correct options' because you selected question 'type':'checkbox'."]
                # if user select question 'type' == 'radio' then it can add only one correct option
                elif question_data.get('type') == 'radio':
                    if correct_answers_count > 1:
                        errors['options'] = [f"Please select only one 'correct option' because you selected question 'type':'radio'."]
            else:
                errors['options'] = ["Please select at least one correct option."]

            # check user must pass at least two options
            if options_data is not None and len(options_data) < 2:
                errors['options'] = ["Please add at least 2 options."]

            # change field into text into title case
            if question_data.get("text"):
                question_data['text'] = question_data['text'].capitalize()

        # default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                # if key not in errors:
                errors[key] = value  # Add new keys to the errors dictionary
                # else:
                #     print(f"value==>{key} ", value)

        # raise validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)
        # print("to_internal_function end.....")
        return validated_data

    def create(self, validated_data):
        # print("validated_data=> ", validated_data)
        # Extract data from validated_data
        quiz_id = validated_data['quizId']
        question_data = validated_data['question']
        options_data = validated_data['options']
        # correct_answers = validated_data['correct_answer']

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

                # 2 Step: create objects
                options = [QuizOptions(question_id=question_instance, **option) for option in options_data]
                # for option in options_data:
                #     options.append()

                # print("options==>", options)
                # step3: create bulk objects
                QuizOptions.objects.bulk_create(options)
            except Exception:
                # Rollback transaction for the current question if any error occurs
                transaction.set_rollback(True)

        return question_instance


class CREATEOptionSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=QuizQuestions.objects.all(),
                                            error_messages={
                                                'does_not_exist': "Invalid question id.",
                                                'incorrect_type': "Incorrect type. Expected a valid question id."
                                            }
                                            )
    option = serializers.CharField(required=True)
    isActive = serializers.BooleanField()
    correctOption = serializers.BooleanField(default=False)

    class Meta:
        fields = ['question_id', 'option', "isActive", "correctOption", "order"]
        model = QuizOptions

    def to_internal_value(self, data):
        question_id = data.get('question_id')
        option = data.get('option')
        errors = {}
        # check quiz.startDate > today date or not
        if question_id:
            try:
                quiz_instance = QuizQuestions.objects.get(id=question_id).quiz_id
                print("quiz_instance")
                quiz_startDate_greate_then_todayDate = compare_dates(
                    end_date=quiz_instance.startDate.strftime(datetime_format))
                quiz_endDate_greater_then_todayDate = compare_dates(
                    end_date=quiz_instance.endDate.strftime(datetime_format))

                if quiz_startDate_greate_then_todayDate and quiz_endDate_greater_then_todayDate:
                    raise serializers.ValidationError({
                        'quiz_id': ["Quiz has ended now you can't add more options."]
                    })
                elif quiz_startDate_greate_then_todayDate:
                    raise serializers.ValidationError({
                        'quiz_id': ["Quiz has started now you can't add more options."]
                    })
            except QuizQuestions.DoesNotExist:
                # print('error in quiz instance serializer')
                pass
            except ValueError:
                # print('error in quiz instance serializer')
                pass

        if option:
            filtered_data_count = QuizOptions.objects.filter(question_id=question_id, option__iexact=option.strip()).count()
            if filtered_data_count > 0:
                errors['option'] = [f"This option is already exist."]

        # default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # raise validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data

    def create(self, validated_data):
        instance = QuizOptions.objects.create(**validated_data)
        # check no. of options are correct
        filtered_data = QuizOptions.objects.filter(question_id=instance.question_id.id, correctOption=True).count()
        # Get the associated QuizQuestions instance
        question_instance = instance.question_id

        if filtered_data >= 2:
            question_instance.type = 'checkbox'
            question_instance.isActive = True
        elif filtered_data == 1:
            question_instance.type = 'radio'
            question_instance.isActive = True
        elif filtered_data == 0:
            question_instance.isActive = False
        question_instance.save()  # Save the modified instance to update the 'type' field
        return instance

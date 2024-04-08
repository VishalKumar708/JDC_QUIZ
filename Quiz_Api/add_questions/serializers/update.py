from rest_framework import serializers


from ...models import QuizQuestions, QuizOptions, Quiz

from django.db.models import Q
from utils.validators import is_given_date_greater_than_or_equal_to_today
from django.conf import settings

datetime_format = getattr(settings, 'DEFAULT_DATE_FORMAT', "%d/%m/%Y")


class UPDATEQuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False, source='question')
    level = serializers.CharField(required=False)
    isActive = serializers.BooleanField(required=False)

    class Meta:
        model = QuizQuestions
        fields = ["text", "level", "isActive"]

    def to_internal_value(self, data):
        quiz_id = self.context.get('quiz_id')
        question_id = self.context.get('question_id')
        question_text = data.get('text')

        errors = {}
        # print("quiz_id=> ", quiz_id)
        # print("question_id=> ", question_id)
        # print("question_text=> ", question_text)
        #

        try:
            quiz_instance = quiz_id
            quiz_startDate_greate_then_todayDate = not is_given_date_greater_than_or_equal_to_today(
                quiz_instance.startDate.strftime(datetime_format))
            quiz_endDate_greater_then_todayDate = not is_given_date_greater_than_or_equal_to_today(
                quiz_instance.endDate.strftime(datetime_format))

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

        if quiz_id is not None and question_text:
            filtered_data = QuizQuestions.objects.filter(Q(question__icontains=question_text.strip(), quiz_id=quiz_id), ~Q(id=question_id)).count()
            if filtered_data > 0:
                errors['text'] = ["This question is already added."]


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

        # raise validation errors
        if errors:
            raise serializers.ValidationError(errors)

        return validated_data


class UPDATEOptionSerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(required=False)
    order = serializers.IntegerField(required=False)
    option = serializers.CharField(required=False)
    correctOption = serializers.BooleanField(required=False)

    class Meta:
        fields = ["option", "isActive", "order", "correctOption"]
        model = QuizOptions

    def to_internal_value(self, data):
        option_text = data.get('option')
        question_id = self.context.get('question_id')
        errors = {}
        if question_id:
            try:
                quiz_instance = question_id.quiz_id
                print("quiz_instance")
                quiz_startDate_greate_then_todayDate = not is_given_date_greater_than_or_equal_to_today(
                    quiz_instance.startDate.strftime(datetime_format))
                quiz_endDate_greater_then_todayDate = not is_given_date_greater_than_or_equal_to_today(
                    quiz_instance.endDate.strftime(datetime_format))

                if quiz_startDate_greate_then_todayDate and quiz_endDate_greater_then_todayDate:
                    raise serializers.ValidationError({
                        'quiz_id': ["Quiz has ended now you can't update options."]
                    })
                elif quiz_startDate_greate_then_todayDate:
                    raise serializers.ValidationError({
                        'quiz_id': ["Quiz has started now you can't update options."]
                    })
            except QuizQuestions.DoesNotExist:
                # print('error in quiz instance serializer')
                pass
            except ValueError:
                # print('error in quiz instance serializer')
                pass

        if option_text:
            filtered_data = QuizOptions.objects.filter(~Q(id=self.context.get('answer_id')), Q(option__iexact=option_text.strip(), question_id=question_id)).count()
            # print("filtered_data => ", filtered_data)
            if filtered_data > 0:
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

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        # change the question type
        # Get the associated QuizQuestions instance
        question_instance = instance.question_id
        # check no. of options are correct
        filtered_data = QuizOptions.objects.filter(question_id=instance.question_id.id,
                                                   correctOption=True).count()
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

from rest_framework import serializers
from django.conf import settings
from utils.validators import is_startDate_greater_than_or_equal_to_endDate
from ..models import *

datetime_format = getattr(settings, 'DEFAULT_DATE_FORMAT', "%d/%m/%Y")


class CreateQuizSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(input_formats=(datetime_format,))
    endDate = serializers.DateField(input_formats=(datetime_format,))
    resultDate = serializers.DateField(input_formats=(datetime_format,))

    class Meta:
        fields = ["title", "startDate", "endDate", "resultDate", "prize", "duration",
                    "organization_id", "order"]
        model = Quiz

    def to_internal_value(self, data):
        errors = {}
        validated_data = None
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        result_date = data.get('resultDate')

        # print("start_date=> ", start_date)
        # print("end_date=> ", end_date)
        # print("result_date=> ", result_date)

        # check startDate is greater than or equal to endDate
        try:
            if not is_startDate_greater_than_or_equal_to_endDate(end_date, start_date):
                errors['endDate'] = [f"'endDate', should be greater then or equal to 'startDate'."]
        except ValueError:
            pass

        # check resultDate is greater than or equal to startDate and endDate
        try:
            # print("startDate is greater then or equalDate=> ", is_startDate_greater_than_or_equal_to_endDate(result_date, start_date))
            # print("resultDate is greater than or equal endDate=> ", is_startDate_greater_than_or_equal_to_endDate(result_date, end_date))
            if not is_startDate_greater_than_or_equal_to_endDate(result_date, end_date):
                errors['resultDate'] = [f"'resultDate' should be greater then or equal to 'startDate' and 'endDate' "]
        except ValueError:
            print("value error occured in serializer")
            pass

        # default validation
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


class UpdateQuizSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(input_formats=(datetime_format,), required=True)
    endDate = serializers.DateField(input_formats=(datetime_format,), required=True)
    resultDate = serializers.DateField(input_formats=(datetime_format,), required=True)

    class Meta:
        fields = ["title", "startDate", "endDate", "resultDate", "prize", "duration",
                    "organization_id", "order", "isVerified", "isActive"]
        model = Quiz

    def to_internal_value(self, data):
        errors = {}
        validated_data = None
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        result_date = data.get('resultDate')
        is_verified = data.get('isVerified')
        quiz_instance = self.context.get('quiz_instance')

        # print("is_Verified=> ", is_verified)
        try:
            value_type = type(is_verified)
            if (value_type is bool and is_verified) or (value_type is str and is_verified.lower() == "true"):
                total_questions = quiz_instance.quiz_questions.filter(isActive=True).count()
                # print("total questions==> ", total_questions)
                if total_questions < 1:
                    raise serializers.ValidationError({'isVerified': [f"This Quiz has not any active question so you can't approve this."]})
        except TypeError:
            pass
        # print("condition runnin...")
        # check startDate is greater than or equal to endDate
        try:
            if not is_startDate_greater_than_or_equal_to_endDate(end_date, start_date):
                errors['endDate'] = [f"'endDate', should be greater then or equal to 'startDate'."]
        except ValueError:
            pass

        # check resultDate is greater than or equal to startDate and endDate
        try:
            if end_date and result_date:
                if not is_startDate_greater_than_or_equal_to_endDate(result_date, end_date):
                    errors['resultDate'] = [f"'resultDate' should be greater then or equal to 'startDate' and 'endDate'"]
        except ValueError:
            pass

        # default validation
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


class GETAllQuizSerializer(serializers.ModelSerializer):
    # startDate = serializers.DateField(input_formats=(datetime_format,))
    endDate = serializers.SerializerMethodField()
    resultDate = serializers.SerializerMethodField()
    startDate = serializers.SerializerMethodField()

    # custom field to get 'questions count'
    totalQuestions = serializers.IntegerField()

    class Meta:
        fields = ["id", "title", "startDate", "endDate", "resultDate", "prize", "duration", "totalQuestions",
                    "organization_id", "order", "isActive", "isVerified"]
        model = Quiz

    def get_startDate(self, instance):
        return instance.startDate.strftime(datetime_format)

    def get_endDate(self, instance):
        return instance.endDate.strftime(datetime_format)

    def get_resultDate(self, instance):
        return instance.resultDate.strftime(datetime_format)





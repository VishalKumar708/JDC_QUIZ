
from rest_framework import serializers
from masterApi.models import MstFeedbackTitle
from django.db.models import Q

from utils.base_serializer import BaseSerializer


class CREATEFeedbackTitleSerializer(BaseSerializer):

    class Meta:
        model = MstFeedbackTitle
        fields = ['title', 'order']

    def to_internal_value(self, data):
        title = data.get('title')

        errors = {}
        if title:
            filtered_obj_count = MstFeedbackTitle.objects.filter(title__iexact=title.strip()).count()
            if filtered_obj_count > 0:
                errors['title'] = [f"'{title}' is already exist."]

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

        # return all validations errors
        if errors:
            raise serializers.ValidationError(errors)

        return validated_data


class UPDATEFeedbackTitleSerializer(BaseSerializer):
    class Meta:
        model = MstFeedbackTitle
        fields = ['title', 'order', 'isActive']

    def to_internal_value(self, data):
        title = data.get('title')
        id = self.context.get('id')
        errors = {}
        if title:
            filtered_obj_count =MstFeedbackTitle.objects.filter(Q(title__iexact=title.strip()), ~Q(id=id)).count()
            if filtered_obj_count > 0:
                errors['bloodGroupName'] = [f"'{title}' is already exist."]

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

        # return all validations errors
        if errors:
            raise serializers.ValidationError(errors)

        return validated_data
        # return super().to_internal_value(data)

    # def validate(self, data):
    #     # Check if at least one field is being updated
    #     updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
    #     if len(updated_fields) == 0:
    #         raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
    #     return data


class GETFeedbackTitleByIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstFeedbackTitle
        fields = ['id', 'title', 'order', 'isActive']


class GETAllFeedbackTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstFeedbackTitle
        fields = ['id', 'title', 'order']


class GETAllFeedbackTitleForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstFeedbackTitle
        fields = ['id', 'title']

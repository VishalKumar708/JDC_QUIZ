from rest_framework import serializers
from masterApi.models import MstMaritalStatus
from django.db.models import Q
from utils.base_serializer import BaseSerializer

class CREATEMaritalStatusSerializer(BaseSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['id', 'maritalStatusName', 'order']


    def to_internal_value(self, data):
        maritalStatusName = data.get('maritalStatusName')
        errors = {}
        if maritalStatusName:
            filtered_obj_count = MstMaritalStatus.objects.filter(maritalStatusName__iexact=maritalStatusName.strip()).count()
            if filtered_obj_count > 0:
                errors['maritalStatusName'] = [f"'{maritalStatusName}' is already exist."]

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


class UPDATEMaritalStatusSerializer(BaseSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['maritalStatusName', 'order', 'isActive']

    def to_internal_value(self, data):
        maritalStatusName = data.get('maritalStatusName')
        id = self.context.get('id')
        errors = {}
        if maritalStatusName:
            filtered_obj_count = MstMaritalStatus.objects.filter(Q(maritalStatusName__iexact=maritalStatusName.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                errors['maritalStatusName'] = [f"'{maritalStatusName}' is already exist."]

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
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data


class GETMaritalStatusByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['id', 'maritalStatusName', 'order', 'isActive']


class GETAllMaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['id', 'maritalStatusName', 'order']


class GETAllMaritalStatusForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['id', 'maritalStatusName']

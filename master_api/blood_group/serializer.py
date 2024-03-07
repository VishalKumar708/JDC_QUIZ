
from rest_framework import serializers
from masterApi.models import MstBloodGroup
from django.db.models import Q
from utils.base_serializer import BaseSerializer
import re
from utils.validators import is_valid_blood_group


class CREATEBloodGroupSerializer(BaseSerializer):

    class Meta:
        model = MstBloodGroup
        fields = ['bloodGroupName', 'order']


    def to_internal_value(self, data):
        bloodGroupName = data.get('bloodGroupName')

        errors = {}
        if bloodGroupName:
            if is_valid_blood_group(bloodGroupName):
                filtered_obj_count = MstBloodGroup.objects.filter(bloodGroupName__iexact=bloodGroupName.strip()).count()
                if filtered_obj_count > 0:
                    errors['bloodGroupName'] = [f"'{bloodGroupName}' is already exist."]
            else:
                errors['bloodGroupName'] = [f"Invalid BloodGroup Name."]
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

        # validated_data['isActive'] = True

        return validated_data


class UPDATEBloodGroupSerializer(BaseSerializer):

    class Meta:
        model = MstBloodGroup
        fields = ['bloodGroupName', 'order', 'isActive']

    def to_internal_value(self, data):
        bloodGroupName = data.get('bloodGroupName')
        id = self.context.get('id')
        errors = {}
        if bloodGroupName:
            if is_valid_blood_group(bloodGroupName):
                filtered_obj_count = MstBloodGroup.objects.filter(Q(bloodGroupName__iexact=bloodGroupName.strip()), ~Q(id=id)).count()
                if filtered_obj_count > 0:
                    errors['bloodGroupName'] = [f"'{bloodGroupName}' is already exist."]
            else:
                errors['bloodGroupName'] = [f"Invalid BloodGroup Name."]
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

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data


class GETBloodGroupByIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstBloodGroup
        fields = ['id', 'bloodGroupName', 'order', 'isActive']


class GETAllBloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstBloodGroup
        fields = ['id', 'bloodGroupName', 'order']


class GETAllBloodGroupForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstBloodGroup
        fields = ['id', 'bloodGroupName']

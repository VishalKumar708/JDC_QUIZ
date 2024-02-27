from rest_framework import serializers
from User.models import User


class BaseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        self.set_created_by(user)
        print('base serializer ==> create method called')
        # save user object
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        self.set_updated_by(user)
        print('base serializer ==> update method called')
        # save user object
        user.save()
        return user

    def set_created_by(self, instance):
        user = self.get_user_object_from_context(user=instance)
        instance.createdBy = user

    def set_updated_by(self, instance):
        user = self.get_user_object_from_context(user=instance)
        instance.updatedBy = user

    def get_user_object_from_context(self, user):
        user_id_by_token = self.context.get('user_id_by_token')
        try:
            if user_id_by_token:
                user_object = User.objects.get(id=user_id_by_token)
                print('user object get from jwt token==> ', user_object)
            else:
                user_object = user
                print('use user current object ==> ', user_object)
        except User.DoesNotExist:
            user_object = None
        print('return user object==> ', user_object)
        return user_object


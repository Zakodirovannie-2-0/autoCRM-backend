from django.conf import settings
from rest_framework import serializers
from accounts.models import *


class UserSerializer(serializers.ModelSerializer):
    avatar_alt = serializers.SerializerMethodField(method_name='get_avatar_alt', read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(UserSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)

            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.is_owner = validated_data.get('is_owner', instance.is_owner)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone_number', 'first_name', 'last_name', 'avatar', 'avatar_alt', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_avatar_alt(self, obj):
        if not obj.avatar:
            return ""
        return 'http://127.0.0.1:8000/media/' + str(obj.avatar)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'date_joined']



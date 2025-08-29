from rest_framework import serializers
from django.contrib.auth.models import User

from django.contrib.auth.password_validation import validate_password




class PublicUserSerializer(serializers.ModelSerializer):
    date_of_membership = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "date_of_membership"]

    def get_date_of_membership(self, obj):
        return obj.date_joined.date() if obj.date_joined else None


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        validate_password(password, user)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            validate_password(password, instance)
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        validate_password(password, user)
        user.set_password(password)
        user.save()
        return user

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework_jwt.settings import api_settings
from .models import *
from django.contrib.auth.models import update_last_login
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from rest_framework import status

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


def password_check(passwd):
    if len(passwd) < 8:
        raise serializers.ValidationError('length should be at least 8')

    if not any(char.isupper() for char in passwd):
        raise serializers.ValidationError('Password should have at least one uppercase letter')

    if not any(char.islower() for char in passwd):
        raise serializers.ValidationError('Password should have at least one uppercase letter')

    return True


def phone_number_check(phone):
    if len(str(phone)) < 10:
        raise serializers.ValidationError('phone number must be 10 digit')
    elif len(str(phone)) > 10:
        raise serializers.ValidationError('phone number must be 10 digit')
    return True

def validate_pincode(obj):
    if obj:
        if len(str(obj)) < 6:
            raise serializers.ValidationError('pincode must be 6 digit')
        elif len(str(obj)) > 6:
            raise serializers.ValidationError('pincode must be 6 digit')
        return True

class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(validators=[validate_password])
    username = serializers.CharField()
    full_name = serializers.CharField()
    phone_number = serializers.IntegerField(validators=[phone_number_check])
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    pincode = serializers.CharField(validators=[validate_pincode])

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            obj = password_check(password)
            if obj:
                return attrs

            else:
                return False

    def create(self, validated_data):
        user = User()
        user.email = validated_data.get('email')
        user.password = make_password(validated_data.get('password'))
        user.username = validated_data.get('username')
        user.full_name = validated_data.get('full_name')
        user.phone = validated_data.get('phone_number')
        user.address = validated_data.get('address')
        user.city = validated_data.get('city')
        user.state = validated_data.get('state')
        user.country = validated_data.get('country')
        user.pincode = validated_data.get('pincode')
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    userEmail = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)


class ContentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    body = serializers.CharField(max_length=300)
    summary = serializers.CharField(max_length=60)
    document = serializers.FileField()
    is_author = serializers.BooleanField(default=False)

    class Meta:
        model = Content
        fields = ["title", "body", "summary", "document", "is_author"]

    def create(self, validated_data):
        return Content.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `AttachmentMROItemObject` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.document = validated_data.get('document', instance.document)
        instance.save()

        return instance


class ContentGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ["id","title", "body", "summary", "document"]
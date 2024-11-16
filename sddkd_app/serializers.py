from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from  dj_rest_auth.registration.serializers import RegisterSerializer

from .models import Question


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    def save(self, request):
        return super().save(request)


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True}
#         }
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data['username'], validated_data['email'], validated_data['password']
#         )
#         user.first_name = validated_data['first_name']
#         user.last_name = validated_data['last_name']
#         user.save()
#         return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
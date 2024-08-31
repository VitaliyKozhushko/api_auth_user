from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=False,
    validators=[UniqueValidator(queryset=User.objects.all())],
    allow_blank=True
  )

  phone = serializers.CharField(
    required=False,
    allow_blank=True
  )

  password = serializers.CharField(
    write_only=True,
    validators=[validate_password],
    required=True
  )

  repeat_password = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields =('username', 'phone', 'email', 'password', 'repeat_password')

  def validate(self, attrs):
    if attrs['password'] != attrs['repeat_password']:
      raise serializers.ValidationError({'password': 'Пароли не совпадают'})
    return attrs

  def create(self, validated_data):
    user = User(
      username=validated_data['username'],
      phone=validated_data.get('phone') or None,
      email=validated_data.get('email') or None
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'is_mentor']
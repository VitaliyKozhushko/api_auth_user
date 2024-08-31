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
    fields =('username', 'phone', 'email', 'password', 'repeat_password', 'is_mentor')

  def validate(self, attrs):
    if attrs['password'] != attrs['repeat_password']:
      raise serializers.ValidationError({'password': 'Пароли не совпадают'})
    return attrs

  def create(self, validated_data):
    user = User(
      username=validated_data['username'],
      phone=validated_data.get('phone') or None,
      email=validated_data.get('email') or None,
      is_mentor=validated_data.get('is_mentor') or False
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'is_mentor']

class ActualUserSerializer(serializers.ModelSerializer):
  username = serializers.CharField(required=False)

  class Meta:
    model = User
    fields = ['username', 'phone', 'email', 'is_mentor']

  def update(self, instance, validated_data):
    for attr, value in validated_data.items():
      setattr(instance, attr, value)

    instance.save()
    return instance

class ChangePasswordSerializer(serializers.Serializer):
  old_password = serializers.CharField(required=True, write_only=True)
  new_password = serializers.CharField(required=True, write_only=True)
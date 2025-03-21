from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'avatar']
        read_only_fields = ['id', 'date_joined']

    def get_avatar(self, obj):
        if hasattr(obj, 'myuser') and obj.myuser.link:
            return obj.myuser.link
        return None

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        MyUser.objects.create(user=user)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(required=False, write_only=True)
    bio = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'bio']

    def update(self, instance, validated_data):
        avatar = validated_data.pop('avatar', None)
        bio = validated_data.pop('bio', None)

        # Update MyUser fields if provided
        if avatar or bio:
            myuser = instance.myuser
            if avatar:
                myuser.link = avatar
            if bio:
                myuser.bio = bio
            myuser.save()

        # Update User fields
        return super().update(instance, validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs 
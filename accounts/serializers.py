from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import MyUser
from thread.models import Thread, Follow

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'avatar', 'is_followed']
        read_only_fields = ['id', 'date_joined']

    def get_avatar(self, obj):
        if hasattr(obj, 'myuser') and obj.myuser.link:
            return obj.myuser.link
        return None

    def get_is_followed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if request.user == obj:
                return False
            from thread.models import Follow
            return Follow.objects.filter(follower=request.user, followed=obj).exists()
        return False

class UserDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    threads = serializers.SerializerMethodField()
    reposted_threads = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'avatar', 
                 'threads', 'reposted_threads', 'is_followed', 'followers_count']
        read_only_fields = ['id', 'date_joined']

    def get_avatar(self, obj):
        if hasattr(obj, 'myuser') and obj.myuser.link:
            return obj.myuser.link
        return None
        
    def get_threads(self, obj):
        from thread.serializers import ThreadSerializer
        threads = Thread.objects.filter(user=obj)
        return ThreadSerializer(threads, many=True, context=self.context).data
        
    def get_reposted_threads(self, obj):
        from thread.serializers import ThreadSerializer
        reposted_threads = obj.reposted_threads.all()
        return ThreadSerializer(reposted_threads, many=True, context=self.context).data
        
    def get_is_followed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if request.user == obj:  # User can't follow themselves
                return False
            return Follow.objects.filter(follower=request.user, followed=obj).exists()
        return False
        
    def get_followers_count(self, obj):
        return Follow.objects.filter(followed=obj).count()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'status': 'error',
                'errors': {'password': 'Password fields didn\'t match.'}
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        MyUser.objects.get_or_create(user=user)
        return user  # Return user object directly

    def to_representation(self, instance):
        # Wrap the response with status here
        data = super().to_representation(instance)
        return {
            'status': 'success',
            'data': data
        }

class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(required=False, write_only=True)
    bio = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'bio']

    def update(self, instance, validated_data):
        try:
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
            user = super().update(instance, validated_data)
            return {
                'status': 'success',
                'data': UserSerializer(user).data
            }
        except Exception as e:
            if isinstance(e, serializers.ValidationError):
                raise e
            raise serializers.ValidationError({
                'status': 'error',
                'errors': str(e)
            })

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                'status': 'error',
                'errors': {
                    'new_password': 'Password fields didn\'t match.'
                }
            })
        return attrs 
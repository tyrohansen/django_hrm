from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from accounts.models import Profile, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name','is_active','is_staff','date_joined')


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            write_only=True,
            required=True, 
            validators=[UniqueValidator(queryset=User.objects.all(), message="username already in use"),]
            )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model= User
        fields =('username','email','password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
        

class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate(self, attr):
       validate_password(attr['new_password'])
       return attr


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    def validate(self, attr):
       validate_password(attr['new_password'])
       return attr


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    user = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attr):
       validate_password(attr['password'])
       return attr


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields ='__all__'
        read_only_fields=('user','created')
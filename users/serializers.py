# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, FreelanceProfile, ClientProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        if attrs['role'] not in ['client', 'freelance']:
            raise serializers.ValidationError({"role": "Rôle invalide."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class FreelanceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelanceProfile
        fields = ('id', 'bio', 'skills', 'hourly_rate', 'portfolio_url', 'avatar', 'updated_at')
        read_only_fields = ('id', 'updated_at')


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ('id', 'bio', 'company', 'website', 'avatar', 'updated_at')
        read_only_fields = ('id', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    freelance_profile = FreelanceProfileSerializer(read_only=True)
    client_profile = ClientProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role',
                  'date_joined', 'freelance_profile', 'client_profile')
        read_only_fields = ('id', 'date_joined', 'role')



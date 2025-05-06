from rest_framework import serializers
from django.contrib.auth import get_user_model
from households.models import Household
from .models import PendingInvitation

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[('admin', 'admin'), ('member', 'member')])
    household = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'birthdate', 'role', 'household']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        role = attrs.get('role')
        household_name = attrs.get('household')

        if role == 'admin':
            if Household.objects.filter(name=household_name).exists():
                raise serializers.ValidationError("Household name already exists.")
        else:
            if not Household.objects.filter(name=household_name).exists():
                raise serializers.ValidationError("No household with that name was found.")

        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        household_name = validated_data.pop('household')

        if role == 'admin':
            household = Household.objects.create(name=household_name)
            user = User.objects.create_user(**validated_data, role=role, household=household, is_active=True)
        else:
            household = Household.objects.get(name=household_name)
            PendingInvitation.objects.create(username=validated_data['username'], household=household)
            user = User.objects.create_user(**validated_data, role=role, household=household, is_active=False)

        return user


# Serializer for updating user information from the frontend (e.g., EditUserModal.jsx)
class UserSerializer(serializers.ModelSerializer):
    household_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'birthdate',
            'role',
            'is_active',
            'was_approved',
            'household_name',
        ]

    def get_household_name(self, obj):
        return obj.household.name if obj.household else None
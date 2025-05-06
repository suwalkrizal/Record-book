from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email','password', 'name','role')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        role = validated_data.pop('role', None)
        user = super().create(validated_data)
        if role:
            user.role = role
            user.groups.set([role])  # 🔥 Assign user to selected group
            user.save()
        return user
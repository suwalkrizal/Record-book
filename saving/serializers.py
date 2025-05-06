from rest_framework import serializers
from .models import *

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    member_name = serializers.ReadOnlyField(source='member.name')

    class Meta:
        model = Record
        fields = ['id', 'month', 'member', 'member_name', 'saving_amount']


class DepositedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositedBy
        fields = '__all__'


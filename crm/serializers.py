from rest_framework import serializers

from accounts.serializers import UserSerializer
from crm.models import *


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'owner', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'business', 'curator', 'name', 'schedule', 'description']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'project', 'customer', 'date', 'stage', 'price_sum']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'employee', 'date', 'date_deadline', 'description', 'stage', 'status']


class EmailSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSample
        fields = ['id', 'text']


class ProjectEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEmail
        fields = ['id', 'project', 'email_sample']


class EmailSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSend
        fields = ['id', 'email_sample', 'customer', 'time', 'send_status']


class CustomerActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAction
        fields = ['id', 'customer', 'order', 'time', 'action']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'task', 'user', 'time_add', 'description']


class EmployeeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProject
        fields = ['employee', 'project', 'role']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'business', 'role']


class UserInProjectSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EmployeeProject
        fields = ['employee', 'user', 'role']

    def get_user(self, obj):
        user_serializer = UserSerializer(obj.employee.user)
        return user_serializer.data

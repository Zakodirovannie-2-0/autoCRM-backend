from rest_framework import serializers

from accounts.serializers import UserSerializer
from crm.models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'date', 'stage', 'price_sum']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'employee', 'date', 'date_deadline', 'description', 'stage', 'status']


class EmailSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSample
        fields = ['id', 'text']


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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'role']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description']
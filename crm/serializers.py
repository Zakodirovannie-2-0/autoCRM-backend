from rest_framework import serializers
from crm.models import *


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'owner', 'name']


class BusinessEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessEmployee
        fields = ['id', 'business', 'employee']


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
        fields = ['id', 'project', 'employee', 'date', 'description', 'stage', 'status']


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

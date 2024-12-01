from rest_framework import serializers

from accounts.serializers import UserSerializer, CustomerSerializer
from crm.models import *


class OrderSerializer(serializers.ModelSerializer):
    service_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'service', 'customer', 'date', 'stage', 'price_sum', 'service_price']

    def get_service_price(self, obj):
        return obj.service.price


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
        fields = ['id', 'name', 'description', 'price']


class WidgetSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    email = serializers.EmailField(max_length=100)
    date = serializers.DateTimeField()


class ServiceOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date', 'stage', 'price_sum']

    def get_customer_name(self, obj):
        return obj.name


class OrderListSerializer(serializers.ModelSerializer):
    service_price = serializers.SerializerMethodField()
    customer = CustomerSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Order
        fields = ['id', 'service', 'customer', 'date', 'stage', 'price_sum', 'service_price']

    def get_service_price(self, obj):
        return obj.service.price


class EmailSampleSendSerializer(serializers.Serializer):
    email_list = serializers.ListField(child=serializers.EmailField())
    text = serializers.CharField()

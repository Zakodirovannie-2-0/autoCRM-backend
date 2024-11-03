from django.contrib.admin import action
from django.template.context_processors import request
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from accounts.serializers import CustomerSerializer
from crm.models import *
from crm.serializers import *


def history_save(data, action, *args):
    customer = Customer.objects.get(id=data.get('customer'))
    order = Order.objects.get(id=data.get('id'))
    data_return = data
    if args:
        data_return = args[0]
    action_data = str({'action': action, 'data': data_return})
    action_obj = CustomerAction.objects.create(customer=customer, order=order, action=action_data)
    action_obj.save()


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = []


class BusinessEmployeeViewSet(viewsets.ModelViewSet):
    queryset = BusinessEmployee.objects.all()
    serializer_class = BusinessEmployeeSerializer
    permission_classes = []


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = []


class OrderViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = []

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        history_save(serializer.data, 'create')
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        history_save(serializer.data, 'patch')
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        history_save(serializer.data, 'patch', request.data)
        return Response(serializer.data)


class OrderListViewSet(viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = []

    def list(self, request, business_pk=None):
        business_projects = Project.objects.filter(business=business_pk).values_list('id', flat=True)
        customers_orders = Order.objects.filter(project__in=business_projects)
        self.queryset = customers_orders
        serializer = self.serializer_class(customers_orders, many=True, context={"request": request})
        return Response(serializer.data)


class CustomerHistoryListViewSet(viewsets.GenericViewSet):
    serializer_class = CustomerActionSerializer
    permission_classes = []

    def list(self, request, business_pk=None, customer_pk=None):
        business_projects = Project.objects.filter(business=business_pk).values_list('id', flat=True)
        customers_orders = Order.objects.filter(project__in=business_projects).values_list('id', flat=True)

        actions = CustomerAction.objects.filter(customer=customer_pk).filter(order__in=customers_orders)
        self.queryset = actions
        serializer = self.serializer_class(actions, many=True, context={"request": request})
        return Response(serializer.data)


class CustomerOrderListViewSet(viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = []

    def list(self, request, business_pk=None, customer_pk=None):
        business_projects = Project.objects.filter(business=business_pk).values_list('id', flat=True)
        customers_orders = Order.objects.filter(customer=customer_pk).filter(project__in=business_projects)
        self.queryset = customers_orders
        serializer = self.serializer_class(customers_orders, many=True, context={"request": request})
        return Response(serializer.data)


class ProjectOrderListViewSet(viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = []

    def list(self, request, project_pk=None):
        orders = Order.objects.filter(project=project_pk)
        self.queryset = orders
        serializer = self.serializer_class(orders, many=True, context={"request": request})
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []


class EmailSampleViewSet(viewsets.ModelViewSet):
    queryset = EmailSample.objects.all()
    serializer_class = EmailSampleSerializer
    permission_classes = []


class ProjectEmailViewSet(viewsets.ModelViewSet):
    queryset = ProjectEmail.objects.all()
    serializer_class = ProjectEmailSerializer
    permission_classes = []


class EmailSendViewSet(viewsets.ModelViewSet):
    queryset = EmailSend.objects.all()
    serializer_class = EmailSendSerializer
    permission_classes = []


class CustomerActionViewSet(viewsets.ModelViewSet):
    queryset = CustomerAction.objects.all()
    serializer_class = CustomerActionSerializer
    permission_classes = []


class BusinessCustomersViewSet(viewsets.ViewSet):
    serializer_class = CustomerSerializer
    permission_classes = []

    def list(self, request, business_pk=None):
        business_projects = Business.objects.filter(id=business_pk).values_list('id', flat=True)
        customers_orders = Order.objects.filter(project__in=business_projects).values_list('id', flat=True)
        customers = Customer.objects.filter(id__in=customers_orders)
        serializer = self.serializer_class(customers, many=True, context={"request": request})
        return Response(serializer.data)


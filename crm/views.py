import datetime

from django.http import HttpResponse, Http404
from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from accounts.serializers import CustomerSerializer, UserSerializer
from backend.email_sample_send import emails_send
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


def notification_task(data):
    task = Task.objects.get(id=data.get('id'))
    user = Employee.objects.get(user=data.get('employee')).user
    notification = Notification.objects.create(user=user, task=task, time_add=datetime.datetime.now())
    time_deadline_notification = task.date_deadline - datetime.timedelta(days=1)
    notification_deadline = Notification.objects.create(user=user, task=task, time_add=time_deadline_notification)
    notification.save()
    notification_deadline.save()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
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
    serializer_class = OrderListSerializer
    permission_classes = []

    def list(self, request):
        customers_orders = Order.objects.all()
        self.queryset = customers_orders
        serializer = self.serializer_class(customers_orders, many=True, context={"request": request})
        return Response(serializer.data)


class CustomerHistoryListViewSet(viewsets.GenericViewSet):
    serializer_class = CustomerActionSerializer
    permission_classes = []

    def list(self, request, customer_pk=None):
        customers_orders = Order.objects.all().alues_list('id', flat=True)

        actions = CustomerAction.objects.filter(customer=customer_pk).filter(order__in=customers_orders)
        self.queryset = actions
        serializer = self.serializer_class(actions, many=True, context={"request": request})
        return Response(serializer.data)


class CustomerOrderListViewSet(viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = []

    def list(self, request, customer_pk=None):
        customers_orders = Order.objects.filter(customer=customer_pk)
        self.queryset = customers_orders
        serializer = self.serializer_class(customers_orders, many=True, context={"request": request})
        return Response(serializer.data)


class TasksListViewSet(viewsets.GenericViewSet):
    serializer_class = TaskSerializer
    permission_classes = []

    def list(self, request):
        tasks = Task.objects.all()
        self.queryset = tasks
        serializer = self.serializer_class(tasks, many=True, context={"request": request})
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        notification_task(serializer.data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        #notification_task(serializer.data)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        #notification_task(serializer.data)
        return Response(serializer.data)


class EmailSampleViewSet(viewsets.ModelViewSet):
    queryset = EmailSample.objects.all()
    serializer_class = EmailSampleSerializer
    permission_classes = []


class EmailSendViewSet(viewsets.ModelViewSet):
    queryset = EmailSend.objects.all()
    serializer_class = EmailSendSerializer
    permission_classes = []


class CustomerActionViewSet(viewsets.ModelViewSet):
    queryset = CustomerAction.objects.all()
    serializer_class = CustomerActionSerializer
    permission_classes = []


class CustomersViewSet(viewsets.ViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = []

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True, context={"request": request})
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = []

    def list(self, request):
        self.queryset = self.queryset.filter(time_add__lt=datetime.datetime.now()).order_by('-time_add')
        serializer = self.serializer_class(self.queryset, many=True, context={"request": request})
        return Response(serializer.data)


class UserNotificationView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user is None:
            return HTTP_401_UNAUTHORIZED

        user_notifications = (self.queryset.filter(user=request.user)
                              .filter(time_add__lt=datetime.datetime.now())
                              .order_by('-time_add'))

        serializer = self.serializer_class(user_notifications, many=True, context={"request": request})
        return Response(serializer.data)


class GetEmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = []

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True, context={"request": request})
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = []


class WidgetViewSet(viewsets.ViewSet):
    serializer_class = WidgetSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = get_object_or_404(Service.objects.all(), id=serializer.data.get('service_id'))
        try:
            customer = Customer.objects.get(email=serializer.data.get('email'))
        except Customer.DoesNotExist:
            customer = Customer(email=serializer.data.get('email'))
            customer.save()

        order = Order(service=service, customer=customer, date=serializer.data.get('date'), stage='start')
        order.save()

        return Response(OrderSerializer(order).data)



class ServiceOrdersListViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = []

    def list(self, request):

        serializer = self.serializer_class(self.queryset, many=True, context={"request": request})
        return Response(serializer.data)


class OrderStatusListViewSet(viewsets.ViewSet):
    permission_classes = []

    def list(self, request):
        customers_orders = Order.objects.all()
        self.queryset = customers_orders

        count = len(customers_orders)
        income = sum(map(lambda x: x.price_sum, customers_orders))
        data = {
            "count" : count,
            "income": income
        }

        return Response(data)


class EmailSampleSendViewSet(viewsets.ViewSet):
    serializer_class = EmailSampleSendSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        emails_send(serializer.data.get("email_list"), serializer.data.get("text"))

        return Response(request.data)
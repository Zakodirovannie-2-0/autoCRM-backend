from django.db import models
from accounts.models import User, Customer


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user}'


class Service(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)


class Order(models.Model):
    project = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=50, null=True, blank=True)
    price_sum = models.IntegerField(default=0)


class Task(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateTimeField()
    date_deadline = models.DateTimeField(null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    stage = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)


class EmailSample(models.Model):
    text = models.TextField(max_length=1000, null=True, blank=True)


class EmailSend(models.Model):
    email_sample = models.ForeignKey(EmailSample, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    send_status = models.CharField(max_length=50, null=True, blank=True)


class CustomerAction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(null=True, blank=True)


class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_add = models.DateTimeField()
    description = models.CharField(null=True, blank=True)
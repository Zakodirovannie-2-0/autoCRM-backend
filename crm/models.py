from django.db import models
from accounts.models import User, Customer, Employee


class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class BusinessEmployee(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)


class Project(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    curator = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)


class Order(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=50, null=True, blank=True)
    price_sum = models.IntegerField(default=0)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.CharField(max_length=500, null=True, blank=True)
    stage = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)


class EmailSample(models.Model):
    text = models.TextField(max_length=1000, null=True, blank=True)


class ProjectEmail(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    email_sample = models.ForeignKey(EmailSample, on_delete=models.CASCADE)


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

from django.db import models
from accounts.models import User, Customer, Employee


class Business(models.Model):
    business_id = models.IntegerField(primary_key=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class BusinessEmployee(models.Model):
    business_employee_id = models.IntegerField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE)
    curator_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=50, null=True, blank=True)
    price_sum = models.IntegerField(default=0)


class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.CharField(max_length=500, null=True, blank=True)
    stage = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)


class EmailSample(models.Model):
    email_sample_id = models.IntegerField(primary_key=True)
    text = models.TextField(max_length=1000, null=True, blank=True)


class ProjectEmail(models.Model):
    project_email_id = models.IntegerField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    email_sample_id = models.ForeignKey(EmailSample, on_delete=models.CASCADE)


class EmailSend(models.Model):
    email_send_id = models.IntegerField(primary_key=True)
    email_sample_id = models.ForeignKey(EmailSample, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    send_status = models.CharField(max_length=50, null=True, blank=True)


class CustomerAction(models.Model):
    customer_action_id = models.IntegerField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100, null=True, blank=True)

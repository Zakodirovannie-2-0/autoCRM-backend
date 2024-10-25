"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import *
from crm.views import *


accounts_router = routers.DefaultRouter()
accounts_router.register(r'user', UserViewSet, basename='user')
accounts_router.register(r'customer', CustomerViewSet, basename='customer')
accounts_router.register(r'employee', EmployeeViewSet, basename='employee')

crm_router = routers.DefaultRouter()
crm_router.register(r'business', BusinessViewSet, basename='business')
crm_router.register(r'business_employee', BusinessEmployeeViewSet, basename='business_employee')
crm_router.register(r'project', ProjectViewSet, basename='project')
crm_router.register(r'order', OrderViewSet, basename='order')
crm_router.register(r'task', TaskViewSet, basename='task')
crm_router.register(r'email-sample', EmailSampleViewSet, basename='email-sample')
crm_router.register(r'project-email', ProjectEmailViewSet, basename='project-email')
crm_router.register(r'email-send', EmailSendViewSet, basename='email-send')
crm_router.register(r'customer-action', CustomerActionViewSet, basename='customer-action')


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'accounts/', include(accounts_router.urls)),
    path(r'crm/', include(crm_router.urls)),
    path('crm/business/<int:business_pk>/customers/', BusinessCustomersViewSet.as_view({'get': 'list'})),
    path('crm/business/<int:business_pk>/orders/', OrderListViewSet.as_view({'get': 'list'})),
    path('crm/business/<int:business_pk>/customer/<int:customer_pk>/orders/', CustomerOrderListViewSet.as_view({'get': 'list'})),
    path('crm/business/<int:business_pk>/customer/<int:customer_pk>/history/', CustomerHistoryListViewSet.as_view({'get': 'list'})),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


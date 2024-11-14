from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from accounts.views import *
from crm.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
)

accounts_router = routers.DefaultRouter()
accounts_router.register(r'user', UserViewSet, basename='user')
accounts_router.register(r'customer', CustomerViewSet, basename='customer')


crm_router = routers.DefaultRouter()
crm_router.register(r'business', BusinessViewSet, basename='business')
crm_router.register(r'employee', EmployeeViewSet, basename='employee')
crm_router.register(r'project', ProjectViewSet, basename='project')
crm_router.register(r'order', OrderViewSet, basename='order')
crm_router.register(r'task', TaskViewSet, basename='task')
crm_router.register(r'email-sample', EmailSampleViewSet, basename='email-sample')
crm_router.register(r'project-email', ProjectEmailViewSet, basename='project-email')
crm_router.register(r'email-send', EmailSendViewSet, basename='email-send')
crm_router.register(r'customer-action', CustomerActionViewSet, basename='customer-action')
crm_router.register(r'notification', NotificationViewSet, basename='notification')
crm_router.register(r'employee-project', EmployeeProjectViewSet, basename='employee_project')


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'accounts/', include(accounts_router.urls)),
    path(r'crm/', include(crm_router.urls)),
    path('crm/business/<int:business_pk>/customers/', BusinessCustomersViewSet.as_view({'get': 'list'})),
    path('crm/business/<int:business_pk>/orders/', OrderListViewSet.as_view({'get': 'list'})),
    path('crm/business/<int:business_pk>/employers', GetBusinessEmployeeViewSet.as_view({'get': 'list'})),
    path('crm/project/<int:project_pk>/orders/', ProjectOrderListViewSet.as_view({'get': 'list'})),
    path('crm/project/<int:project_pk>/employers/', GetProjectUsersViewSet.as_view({'get': 'list'})),
    path('crm/project/<int:project_pk>/tasks/', ProjectTasksListViewSet.as_view({'get': 'list'})),
    path('crm/business/<int:business_pk>/customer/<int:customer_pk>/orders/', CustomerOrderListViewSet.as_view({'get': 'list'})),
    path('crm/business/<int:business_pk>/customer/<int:customer_pk>/history/', CustomerHistoryListViewSet.as_view({'get': 'list'})),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/me/', GetUserInfoView.as_view()),
    path('accounts/my-notifications/', UserNotificationView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
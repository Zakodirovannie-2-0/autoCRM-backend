from rest_framework import viewsets, generics
from accounts.models import *
from accounts.serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.http import Http404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = []


class GetUserInfoView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        if request.user is None:
            return Http404

        serializer = self.serializer_class(request.user)

        return Response(serializer.data)




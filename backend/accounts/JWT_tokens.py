from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = dict()
        user_data['id'] = self.user.id
        user_data['first_name'] = self.user.first_name
        user_data['last_name'] = self.user.last_name
        user_data['email'] = self.user.email
        user_data['is_owner'] = self.user.is_owner
        user_data['phone_number'] = self.user.phone_number
        data['user'] = user_data
        return data
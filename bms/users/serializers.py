from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    """
    users = User.objects.all()
    this gives a query set like this, so we use built-in serializer to process it.
    <QuerySet [Username: firstuser, Email: firstuser@gmail.com, is_active: True is_Owner: True, is_employee: True]>
    Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes.
    """

    class Meta:
        model = Users
        # fields = '__all__'
        fields = ('id','username','email','is_owner',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
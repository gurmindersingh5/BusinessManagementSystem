from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView, status

from .serializers import UsersSerializer

"""
in Django, when using class-based views (CBVs) such as those provided by Django REST 
Framework (APIView), you create methods like get(), post(), put(), and delete() to 
handle different HTTP request methods. This is similar to how you specify HTTP 
methods in Flask with methods=['GET', 'POST'].
"""

User = get_user_model() # Users obj to deal with Users Model

class Register(APIView):
    def post(self, request):
        try:
            username = request.GET.get('username')
            email = request.GET.get('email')
            password = request.GET.get('password')
            re_password = request.GET.get('re_password')
            is_owner = request.GET.get('is_owner')

            if is_owner == 'True':
                is_owner = True
                owner_passkey = request.GET.get('owner_passkey')

            if not all([username, email, password, re_password]):
                return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

            if password == re_password:
                if not User.objects.filter(username=username).exists(): #checking it user exists with same username
                    if is_owner == True:
                        User.objects.create_superuser(username=username, email=email, password=password, owner_passkey=owner_passkey)
                        return Response(
                            {'Success': 'Owner User created successfully with Full Privileges'},
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        User.objects.create_user(username, email, password)
                        return Response(
                            {'success': 'User created successfully'},
                            status=status.HTTP_201_CREATED
                        )
                else:
                    return Response(
                            {'Error':f'Cannot create user with username: {username}, user already exists'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
            else:
                return Response(
                            {'Error':f'Password in password and re-password fields does not match!!!'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

        except Exception as e:
            return JsonResponse({'error':str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class GetUsers(APIView):
    def get(self):
        users = User.objects.all()
        # this gives a query set like this, so we use built-in serializer to process it.
        # <QuerySet [Username: firstuser, Email: firstuser@gmail.com, is_active: True is_Owner: True, is_employee: True]>
        # Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes.
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)


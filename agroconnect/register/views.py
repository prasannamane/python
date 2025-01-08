from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from .models import UserProfile
from .serializers import UserSerializer
import requests
import json
from django.http import HttpResponse, JsonResponse

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    mobile_number = serializers.CharField(max_length=15)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_mobile_number(self, value):
        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Invalid mobile number.")
        return value


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            mobile_number = serializer.validated_data['mobile_number']

            # Create a new user
            user = User.objects.create_user(
                username=username, password=password, email=email)

            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(source='profile.mobile_number')

    class Meta:
        model = User
        # Specify the fields you want to display
        fields = ['id', 'username', 'email', 'mobile_number']


class UserListAPIView(APIView):
    def post(self, request):
        users = User.objects.all()  # Fetch all users
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateAPIView(APIView):
    
    def post(self, request):
        print(request.data)
        
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                
                #Call api and store data
                url = "http://localhost:8006/api/register"
                payload = json.dumps({
                  "mobile": user.mobile,
                  "password": user.password
                })
                headers = {
                  'Content-Type': 'application/json',
                  'Cookie': 'connect.sid=s%3AKZ6aABLRkow-8uSkeEWNly7HAJqyUejU.ZX85pAXql9Bc9FyRDRHsPIBkbyRKG8XOddgKn71ymfw'
                }
                
                response = requests.request("POST", url, headers=headers, data=payload)
                
                
    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UserList(APIView):
    def get(self, request):
        url = "http://localhost:8006/api"
        headers = {
            'Cookie': 'connect.sid=s%3ATygarP2qsR1RawP2pf5hTFdhagT8ilxg.a%2BPULAzFttMqkuM1DgQk1syItfpPUL9SWRh%2BjwMKGhY'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Assuming the response is JSON, parse it
            data = response.json()

            # Return a JsonResponse with the data
            return JsonResponse(data)
        except requests.exceptions.RequestException as e:
            # Return a JsonResponse with an error message if there's a network problem
            return JsonResponse({'error': str(e)}, status=500)

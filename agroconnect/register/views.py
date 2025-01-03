from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from .models import UserProfile

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

            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email)
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(source='profile.mobile_number')
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_number']  # Specify the fields you want to display

class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()  # Fetch all users
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

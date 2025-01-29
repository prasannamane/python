from rest_framework import serializers
from .models import Register

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Register
        fields = '__all__'  # Include all fields
        
    # Alternatively, you can specify individual fields
    # fields = ['field1', 'field2', 'field3']  # List specific fields
    
    # Or exclude certain fields
    # exclude = ['field_to_exclude']

    def validate_username(self, value):
        if Register.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        if Register.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value
    
    def validate_mobile(self, value):
        if Register.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("A user with this mobile number already exists.")
        return value

    def validate_mobile_number(self, value):
        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Invalid mobile number.")
        return value

    def validate_password(self, value):
        return value

class UserSigninSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        print('yes')
        fields = ['password', 'mobile']
        
    def validate(self, data):
        mobile = data.get('mobile')
        password = data.get('password')

        # Check if the mobile number exists
        user = Register.objects.filter(mobile=mobile).first()
        
        if user is None:
            raise serializers.ValidationError("Mobile does not exist.")
        
        # Check if the password matches
        if user.password != password:
            raise serializers.ValidationError("Invalid password.")

        return data

# from django.contrib.auth.models import User
from master.models import User, RegToken
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer untuk User profile dengan informasi registration token
    """
    reg_token_info = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'full_name', 'phone', 'reg_token_info', 'date_joined']
    
    def get_reg_token_info(self, obj):
        """Get registration token information"""
        if obj.reg_token:
            return {
                'token_name': obj.reg_token.name,
                'token_code': obj.reg_token.token_code,
                'registered_at': obj.created_at
            }
        return None


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Enhanced User Registration Serializer dengan Registration Token validation
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    
    password2 = serializers.CharField(
        write_only=True, 
        required=True
    )
    
    # NEW: Registration token field
    token_registrasi = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Token registrasi yang diperlukan untuk mendaftar"
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 
                  'last_name', 'phone', 'token_registrasi']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_token_registrasi(self, value):
        """
        Validate registration token
        """
        try:
            token = RegToken.objects.get(token_code=value)
        except RegToken.DoesNotExist:
            raise serializers.ValidationError("Token registrasi tidak valid.")
        
        # Check if token is still valid
        is_valid, message = token.is_valid()
        if not is_valid:
            raise serializers.ValidationError(f"Token registrasi tidak valid: {message}")
        
        return value

    def validate(self, attrs):
        """
        Validate password confirmation and overall data
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password tidak cocok."
            })
        
        return attrs

    def create(self, validated_data):
        """
        Create user dengan registration token
        """
        # Get and validate token
        token_code = validated_data.pop('token_registrasi')
        validated_data.pop('password2')  # Remove password confirmation
        
        try:
            reg_token = RegToken.objects.get(token_code=token_code)
        except RegToken.DoesNotExist:
            raise serializers.ValidationError({
                "token_registrasi": "Token registrasi tidak valid."
            })
        
        # Double-check token validity (could have changed between validate and create)
        is_valid, message = reg_token.is_valid()
        if not is_valid:
            raise serializers.ValidationError({
                "token_registrasi": f"Token registrasi tidak valid: {message}"
            })
        
        # Create user
        password = validated_data.pop('password')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data.get('phone', ''),
            reg_token=reg_token  # Assign registration token
        )
        
        user.set_password(password)
        user.save()
        
        # Use the token (increment usage counter)
        reg_token.use_token()
        
        return user


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer untuk change password
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Password baru tidak cocok."
            })
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer untuk password reset request
    """
    email = serializers.EmailField(required=True)


class RegTokenValidationSerializer(serializers.Serializer):
    """
    Serializer untuk validasi registration token tanpa membuat user
    """
    token_code = serializers.CharField(required=True)
    
    def validate_token_code(self, value):
        """
        Validate registration token
        """
        try:
            token = RegToken.objects.get(token_code=value)
        except RegToken.DoesNotExist:
            raise serializers.ValidationError("Token registrasi tidak ditemukan.")
        
        # Check if token is still valid
        is_valid, message = token.is_valid()
        if not is_valid:
            raise serializers.ValidationError(f"Token tidak valid: {message}")
        
        return value
    
    def to_representation(self, instance):
        """
        Return token information if valid
        """
        token_code = self.validated_data['token_code']
        token = RegToken.objects.get(token_code=token_code)
        
        return {
            'token_name': token.name,
            'token_code': token.token_code,
            'remaining_usage': token.remaining_usage,
            'expires_at': token.expires_at,
            'is_valid': True,
            'message': 'Token valid dan dapat digunakan untuk registrasi'
        }

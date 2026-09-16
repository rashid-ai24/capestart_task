"""
ClassHub Authentication Serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone_number', 'profile_picture', 'date_of_birth',
            'gender', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'password', 'password_confirm',
            'role', 'phone_number', 'date_of_birth', 'gender'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'Passwords do not match.'})
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting password reset."""
    
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            # Don't reveal if user exists or not
            pass
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset."""
    
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'Passwords do not match.'})
        
        # Validate token
        from apps.authentication.models import PasswordResetToken
        try:
            reset_token = PasswordResetToken.objects.get(
                token=attrs['token'],
                is_used=False
            )
            if reset_token.is_expired:
                raise serializers.ValidationError({'token': 'Token has expired.'})
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({'token': 'Invalid token.'})
        
        return attrs


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = self.authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('Account is disabled.')
            
            # Check if account is locked
            if user.account_locked_until and user.account_locked_until > timezone.now():
                raise serializers.ValidationError('Account is temporarily locked. Please try again later.')
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Email and password are required.')
        
        return attrs
    
    def authenticate(self, email, password):
        """Authenticate user with email and password."""
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                # Reset failed login attempts on successful login
                user.reset_failed_login()
                return user
            else:
                # Increment failed login attempts
                user.increment_failed_login()
                # Lock account after 5 failed attempts
                if user.failed_login_attempts >= 5:
                    user.account_locked_until = timezone.now() + timedelta(minutes=15)
                    user.save(update_fields=['account_locked_until'])
                return None
        except User.DoesNotExist:
            return None


class MFAEnableSerializer(serializers.Serializer):
    """Serializer for enabling MFA."""
    
    code = serializers.CharField(max_length=6)
    
    def validate_code(self, value):
        # Here you would validate the TOTP code
        # For now, just check it's 6 digits
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError('Invalid MFA code.')
        return value


class MFALoginSerializer(serializers.Serializer):
    """Serializer for MFA login."""
    
    token = serializers.CharField()
    mfa_code = serializers.CharField(max_length=6)
    
    def validate_mfa_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError('Invalid MFA code.')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    full_name = serializers.SerializerMethodField()
    student_profile = serializers.SerializerMethodField()
    faculty_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone_number', 'profile_picture', 'date_of_birth',
            'gender', 'mfa_enabled', 'student_profile', 'faculty_profile',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'role', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_student_profile(self, obj):
        if obj.role == 'student':
            from apps.students.serializers import StudentSerializer
            try:
                student = obj.student_profile
                return StudentSerializer(student).data
            except:
                return None
        return None
    
    def get_faculty_profile(self, obj):
        if obj.is_faculty:
            from apps.students.serializers import FacultySerializer
            try:
                faculty = obj.faculty_profile
                return FacultySerializer(faculty).data
            except:
                return None
        return None

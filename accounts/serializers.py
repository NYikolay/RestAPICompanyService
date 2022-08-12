from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from accounts.models import CustomUser
from accounts.models import Company


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        """ Check if password1 == password2 """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didn\'t match'}
            )
        return attrs

    def create(self, validated_data):
        """
        This method both for workers creation and ADMIN user creation
        If current user has access_token and this user is ADMIN then creating worker and give him ADMIN company
        Else create ADMIN user
        """
        if self.context['request'].user.user_type == 'ADMIN':
            user = CustomUser.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                user_company=self.context['request'].user.user_company,
                user_type='REGULAR'
            )
        else:
            user = CustomUser.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                user_type='ADMIN'
            )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for company model management
    """
    class Meta:
        model = Company
        fields = '__all__'

    def create(self, validated_data):
        """
        Creating and return company object if data is valid
        """
        company = Company.objects.create(
            name=validated_data['name'],
            address=validated_data['address'],
            owner=self.context['request'].user
        )

        company.save()
        return company


class UpdateWorkerSerializer(serializers.ModelSerializer):
    """ Update company worker serializer """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_username(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']

        instance.set_password(validated_data['password'])
        instance.save()

        return instance




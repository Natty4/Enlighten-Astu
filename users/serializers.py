from rest_framework import serializers
from .models import User, Other, Instructor
from dj_rest_auth.registration.serializers import RegisterSerializer



class InstructorRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    verify_url = 'sevenoon.internx.com/'
    class Meta:
        model = Instructor
        fields = ['first_name','last_name', 'username', 'email', 'phone_number', 'campus', 'password', 'password2',]
        extra_kwargs = {
            'password': {
                'write_only':True
            },
            'password2': {
                'write_only':True
            }
        }

    def save(self, request):
        user = Instructor(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone_number=self.validated_data['phone_number'],
           
            campus=self.validated_data['campus'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.is_instructor = True
        user.save()
        
        return user



class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = [  
                    "campus",
                    "profile_pic",
                    "linkedin",
                    "github",
                    "telegram",
                    "is_instructor",]
        read_only_fields = ('is_active', 'is_instructor')

class OtherRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Other
        fields = ['first_name','last_name', 'username', 'email', 'phone_number', 'campus', 'password', 'password2',]
        extra_kwargs = {
            'password': {
                'write_only':True
            },
            'password2': {
                'write_only':True
            }
        }

    def save(self, request):
        user = Other(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone_number=self.validated_data['phone_number'],
           
            campus=self.validated_data['campus'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.is_other = True
        user.save()
        return user



class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = [  
                    "campus",
                    "profile_pic",
                    "linkedin",
                    "github",
                    "telegram",
                    "created_at",
                    "updated_at",
                    "is_other",]
        read_only_fields = ('is_active', 'is_other')





class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name', 'phone_number', 'password', 'password2',]
        extra_kwargs = {
            'password': {
                'write_only':True
            },
            'password2': {
                'write_only':True
            }
        }

    def save(self, request):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone_number=self.validated_data['phone_number'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

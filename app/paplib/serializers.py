from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Mountain, ClimbRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class MountainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mountain
        fields = ['id', 'name', 'prefecture', 'elevation']
    
class ClimbRecordSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = ClimbRecord
        fields = ['id', 'user', 'mountain', 'comment', 'climb_date', 'created_at', 'image']
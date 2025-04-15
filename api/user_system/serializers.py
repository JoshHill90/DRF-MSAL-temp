from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["name"]
        

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', "groups"]
        
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

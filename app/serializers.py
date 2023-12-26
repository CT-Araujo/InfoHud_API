from rest_framework import serializers
from django.contrib.auth.models import User
from .models import*



class UsuariosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password= validated_data['password'],
            first_name = validated_data['first_name']
        )
       
        return user
    
    
class PostagemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Postagens
        fields = '__all__'
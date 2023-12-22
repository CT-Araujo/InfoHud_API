from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests

#///////////////////////////////////////////////////////////////////////////////////////////////

class UsuariosViews(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializers
    
    def list(self, request):
        filtro = request.query_params.get('username', None)
        user = User.objects.filter(username=filtro).exists()
        if filtro:
            if user:
                usuarios = User.objects.filter(username=filtro)
                serialized_data = UsuariosSerializers(usuarios, many=True).data
                return Response(serialized_data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        usuarios = User.objects.all()
        serialized_data = UsuariosSerializers(usuarios, many=True).data
        return Response(serialized_data,status=status.HTTP_200_OK)
        
    
    def get(self, request):
       dados = User.objects.all()
       serialized_data = UsuariosSerializers(dados, many= True).data
       return Response(serialized_data, status= status.HTTP_200_OK)
   
    def post(self,request):
        serializer = UsuariosSerializers(data= request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#////////////////////////////////////////////////////////////////////////////////////////////////
class UsuariosLoginViews(APIView):
    def get(self,request):
        dados = User.objects.all()
        return Response(status= status.HTTP_200_OK)
    
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        existe = User.objects.filter(username = username).exists()
        user = authenticate(username = username, password = password)
        
        if existe:
            if user:

                dados = {
                    'username': username
                }
                return Response(dados, status= status.HTTP_200_OK)
        
            else:
                    return Response(user, status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    
            
#////////////////////////////////////////////////////////////////////////////////////////////////
   
class PostagemViews(APIView):
    def get(self,request):
        filtro = request.query_params.get('criador',None)
        criador = User.objects.filter(username=filtro).exists
        if filtro:
            if criador:
                dados = Postagens.objects.filter(user_nickname=filtro)
                serialized = PostagemSerializers(dados, many = True)
                return Response(serialized.data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            dados = Postagens.objects.all()
            serialized = PostagemSerializers(dados,many = True)
            return Response(serialized.data,status= status.HTTP_200_OK)
    
    def post(self,request):
        serializer = PostagemSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
  
        
    def get_permissions(self):
 
        if self.request.method == 'GET':
            return [AllowAny()]  
        elif self.request.method == 'POST':
            return [IsAuthenticated()] 
        return super().get_permissions()
    

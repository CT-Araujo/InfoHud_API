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
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not (username and password):
            return Response("Informe username e password.", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response("Usuário não encontrado.", status=status.HTTP_404_NOT_FOUND)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response("Credenciais inválidas.", status=status.HTTP_401_UNAUTHORIZED)

     
        url = 'https://infohudapi.onrender.com/token/'
        data_user = {
            'username': username,
            'password': password
        }

        response = requests.post(url, data=data_user)

        if response.status_code == 200:
            token = response.json().get('access')
            dados = {
                'token': token,
                'username': username
            }
            return Response(dados, status=status.HTTP_200_OK)
        else:
            return Response("Erro ao obter token.", status=status.HTTP_400_BAD_REQUEST)
            
    
            
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
    


from django.test import RequestFactory
import requests
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ObjectDoesNotExist
#///////////////////////////////////////////////////////////////////////////////////////////////

class UsuariosViews(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializers
    
    def list(self, request):
        filtro = request.query_params.get('username', None)
        user = User.objects.filter(username=filtro).exists()
        if filtro:
            if user:
                usuarios = User.objects.filter(username = filtro)
                serialized_data = UsuariosSerializers(usuarios, many = True).data
                
                return Response(serialized_data, status = status.HTTP_200_OK)
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        usuarios = User.objects.all()
        serialized_data = UsuariosSerializers(usuarios, many=True).data
        
        return Response(serialized_data,status = status.HTTP_200_OK)
   
    def get(self, request):
       dados = User.objects.all()
       serialized_data = UsuariosSerializers(dados, many= True).data
       return Response(serialized_data, status= status.HTTP_200_OK)
   
    def post(self,request):
        serializer = UsuariosSerializers(data= request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            
            token = obter_token_jwt(username, password)
            dados = {
                "token":token,
                "username": username
            }
            if token:
                return Response(dados, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Falha na autenticação'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk = None):
        if request.method == 'PATCH':
            filtro = request.query_params.get('username', None)
            existe = User.objects.filter(username = filtro).exists()
            
            token = request.headers.get('Authorization')
            
            if existe:
                user = User.objects.get(username = filtro)
                if token:
                    serializer = UsuariosSerializers(user, data= request.data, partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status= status.HTTP_200_OK)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get_permissions(self):
 
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [AllowAny()]  
        elif self.request.method == 'PATCH':  
            return [IsAuthenticated()] 
        return super().get_permissions()
        
#////////////////////////////////////////////////////////////////////////////////////////////////
class UserLoginView(APIView):
    
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        existe = User.objects.filter(username = username).exists()
        dados = {
            'username':username,
            'password': password
        }
        if existe:
            user = authenticate(username= username, password = password)
            if user:
                token = obter_token_jwt(username, password)
                dados = {
                    "token":token,
                    "username":username
                }
                return Response(dados, status = status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status = status.HTTP_404_NOT_FOUND)

def obter_token_jwt(username, password):
    factory = RequestFactory()
    request = factory.post('/token/', {'username': username, 'password': password})
    view = TokenObtainPairView.as_view()
    response = view(request)
    return response.data.get('access')  

#////////////////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////////////////
   
class PostagemViews(APIView):
    def get(self,request):
        filtro_id = request.query_params.get('id',None)
        filtro_categoria = request.query_params.get('categoria',None)
        filtro_criador = request.query_params.get('criador',None)
        criador = User.objects.filter(username = filtro_criador).exists()
        
        
        if filtro_id:
            dados = Postagens.objects.filter(id=filtro_id)
            serialized = PostagemSerializers(dados, many = True)
            return Response(serialized.data, status = status.HTTP_200_OK)
        
        
        if filtro_criador and filtro_categoria:
            if criador:
                dados = Postagens.objects.filter(user_nickname = filtro_criador,categoria = filtro_categoria)
                serialized = PostagemSerializers(dados, many = True)
                return Response(serialized.data, status= status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_404_NOT_FOUND)
        
        if filtro_criador:
            if criador:
                dados = Postagens.objects.filter(user_nickname = filtro_criador)
                serialized = PostagemSerializers(dados, many = True)
                return Response(serialized.data,status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_404_NOT_FOUND)
            
        if filtro_categoria:
            dados = Postagens.objects.filter(categoria = filtro_categoria)
            serialized = PostagemSerializers(dados, many = True)
            return Response(serialized.data,status = status.HTTP_200_OK)
        
        dados = Postagens.objects.all()
        serialized = PostagemSerializers(dados,many = True)
        return Response(serialized.data,status = status.HTTP_200_OK)
    
    
    
    def post(self,request):
        serializer = PostagemSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        get_id = request.data.get('id')
        try:
            dado = Postagens.objects.get(id = get_id)
            dado.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
  
        
    def get_permissions(self):
 
        if self.request.method == 'GET':
            return [AllowAny()]  
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':  
            return [IsAuthenticated()] 
        return super().get_permissions()
    

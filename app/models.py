from django.db import models

class Usuarios(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key= True, editable=True, unique= True)
    username = models.CharField(max_length=40, unique=True, blank= False)
    first_name = models.CharField(max_length=60, blank= False)
    email = models.EmailField(max_length=150,blank= False, unique= True)
    password = models.CharField(blank= False, max_length= 30)
    
    
    
class Postagens(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key= True, editable=True, unique= True)
    titulo = models.CharField(max_length=50, blank= False, null= False)
    subtitulo = models.CharField(max_length=40, blank= False, null= False)
    categoria = models.CharField(max_length=50, blank= False, null= True)
    miniurl = models.CharField(max_length=150, blank= True, null=True)
    conteudo = models.CharField(max_length=500, blank=False, null=True)
    user_nickname = models.CharField(max_length=50, blank=False, editable=True)    
    
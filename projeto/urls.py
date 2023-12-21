
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from app import views

route = routers.DefaultRouter()
route.register(r'Usuarios',views.UsuariosViews,basename='Usuarios')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(route.urls)),
    path('postagem/',views.PostagemViews.as_view(),name='postagem')
]

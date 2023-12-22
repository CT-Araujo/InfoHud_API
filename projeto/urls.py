
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app import views

route = routers.DefaultRouter()
route.register(r'Usuarios',views.UsuariosViews,basename='Usuarios')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(route.urls)),
    path('token/',TokenObtainPairView.as_view(),name='token'),
    path('postagem/',views.PostagemViews.as_view(),name='postagem'),
    path('login/',views.UsuariosLoginViews.as_view(),name='login'),
]

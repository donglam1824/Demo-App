from django.contrib import admin
from django.urls import path, include
from authentication import views
from .views import MyTokenObtainPairView, UserCreateAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserCreateAPIView.as_view(), name='register'),
]
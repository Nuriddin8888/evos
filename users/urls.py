from django.urls import path
from .views import register, login_view, update_profile, verify_view, home, logout_view, profile_view

app_name = 'users'


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("verify/", verify_view, name="verify"),    
    path("home/", home, name="home"),    
    path("logout/", logout_view, name="logout"),    
    path("profile/", profile_view, name="profile"), 
    path('update-profile/', update_profile, name='update_profile'),   
]
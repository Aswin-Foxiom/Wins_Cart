from django.urls import path
from .views import *

urlpatterns = [
    path('UserDetails/',UserView.as_view()),
    path('changestatus/',ChangeStatus.as_view()),
    path('Login/',LoginView.as_view()),
    path('logineduser/',LoginedUser.as_view()),
    path('logout/',LogoutView.as_view()),
]

from django.urls import path
from .views import *

urlpatterns = [
   path('get_all_country/',DialCodeView.as_view())
]

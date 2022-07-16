# Common Importing
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import make_password
from .Validation import *
from rest_framework import status
import json
import datetime
from django.db.models import Q


# For User App
from UserApp.models import *
from UserApp.serializers import *

# For Country App

from CountryApp.serializers import *
from CountryApp.models import *
from django.urls import path
from Resetpassword import views


urlpatterns = [
    path("emailverify/",views.PasswordReset.as_view(), name="request-password-reset",),
    path("password-reset/<str:encoded_pk>/<str:token>/",views.ResetPasswordAPI.as_view(),name="reset-password",),
]

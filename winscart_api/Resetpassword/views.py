
from UserApp.models import UserDetailsModel
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from winscart_api.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from winscart_api.Importedpage import *


from . import serializers


class PasswordReset(ListAPIView):
    

    serializer_class = serializers.EmailSerializer

    def get_queryset(self):
        return None

    def post(self, request):
       
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = UserDetailsModel.objects.filter(username=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "reset-password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            reset_link = f"{self.request.data['sitename']}{reset_url}"

            send_mail("Password Reset ","ok",EMAIL_HOST_USER,[email],fail_silently=True,html_message=reset_link)


           
            return Response({
                 "Message": f"Your password rest link: {reset_link}",
                 "Status" : status.HTTP_200_OK
            })
        else:
            return Response({
                "Message" : "User doesn't exists",
                "Status" : status.HTTP_400_BAD_REQUEST
            })
         

class ResetPasswordAPI(ListAPIView):
   

    serializer_class = serializers.ResetPasswordSerializer

    def get_queryset(self):
        return None

    def patch(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return Response({
            "Message": "Password reset complete",
            "Status"  : status.HTTP_200_OK,
       })
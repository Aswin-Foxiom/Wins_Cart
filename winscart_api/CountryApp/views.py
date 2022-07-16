from functools import partial
from django.shortcuts import render
from winscart_api.Importedpage import *
# Create your views here.

class DialCodeView(ListAPIView):
    serializer_class = DialCodeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        allcodes = DialCodeModels.objects.all()
        return allcodes

    def post(self,request):
        
        serializer = DialCodeSerializer(data=self.request.data,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"Status":status.HTTP_200_OK,"Message" : "Country Code Succesfully Created"})
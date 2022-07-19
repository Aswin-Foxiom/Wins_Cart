from winscart_api.Importedpage import *

# Create your views here.

class UserView(ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        id  =  self.request.GET.get("id","")
        username  =  self.request.GET.get("username","")
        userstatus  =  self.request.GET.get("userstatus","")
        Phonenumber  =  self.request.GET.get("Phonenumber","")
        user = UserDetailsModel.objects.all()
        
        if id : 
            user = user.filter(id=id)
        if username :
            user = user.filter(Q(first_name__icontains = username) | Q(last_name__icontains = username))
        if userstatus:
            user= user.filter(status = userstatus)
        if Phonenumber : 
            user = user.filter(mobile = Phonenumber)
        return user

    def post(self,request):
        user_obj = ""  
        try:      
            id = self.request.data["id"]
        except:
            id = ""   
       
        if id:
            try:
                user = UserDetailsModel.objects.filter(id=id)
                if user.count():
                    user = user.first()
                else:
                    return Response({
                        "Status" : status.HTTP_404_NOT_FOUND,
                        "Message" : "User Not Found"
                    })

                serializer = UserSerializer(user,data=self.request.data,partial=True)
                serializer.is_valid(raise_exception=True)
                try:
                    password = self.request.data['password']
                except:
                    password = ""
                
                if password  :
                    msg="User details and password updated Succesfully"
                    user_obj = serializer.save(password=make_password(password))
                
                else:
                    msg="User details updated Succesfully"
                    user_obj = serializer.save()
                

                
                return Response({
                        "Status":status.HTTP_200_OK,
                        "Message":msg
                    })

            except Exception as e:
              
                return  Response({
                    "Status":status.HTTP_400_BAD_REQUEST,
                    "Message":f"Excepction occured {e}"
                })
        
        else:
            mandatory = ['username','password','mobile','usertype','showpassword']
            data = Validate(self.request.data,mandatory)
            if data == True:
                username_check = UserDetailsModel.objects.filter(username = self.request.data['username'])

                if username_check.count():
                    return Response({
                        "Status" : status.HTTP_406_NOT_ACCEPTABLE,
                        "Message" : "Username Already Registered"
                    })
               
                try:      
                    
                    serializer = UserSerializer(data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                
                    msg = "Created New User"
                    user_obj = serializer.save(password=make_password(self.request.data['password']))

                    return Response({
                        "Status":status.HTTP_200_OK,
                        "Message":msg
                    })

                except Exception as e:
                   
                    if user_obj:
                        user_obj.delete()

                    return  Response({
                        "Status":status.HTTP_400_BAD_REQUEST,
                        "Message":f"Excepction occured {e}"
                    })
            
            else:
                return Response({
                    "Status" : status.HTTP_400_BAD_REQUEST,
                    "Message" : data
                })

    def delete(self,request):
        try:
            id = self.request.data['id']
        except:
            id = ""
       
        if id:
            try:
                
                # id = json.loads(id)
                objects = UserDetailsModel.objects.filter(id=id)

                if objects.count():
                    objects.delete()
                    return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
                else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No records with given id" })

            except:
                return Response({
                    "Status" : status.HTTP_400_BAD_REQUEST,
                    "Message" : "Something Went Wrong"
                })
        else:
            return Response({
                "Status" : status.HTTP_400_BAD_REQUEST,
                "Message" : "No User Found"
            })  


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data,context={'request': request})
        try:
            test = serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            data = UserDetailsModel.objects.get(id=user.id)
            data.last_login = datetime.datetime.now()
            data.save()
            token, created = Token.objects.get_or_create(user=user)
            print(user.is_superuser)
            return Response({
                "Status":status.HTTP_200_OK,
                'token': "Token "+token.key,
                'user_id': user.id,
                'username': user.username,
                'superuser' : user.is_superuser           
                
            })
        except Exception as e:
            return Response({
                "Status":status.HTTP_400_BAD_REQUEST,
                "Message":"Incorrect Username or Password",
            })

class  LoginedUser(ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        id = self.request.user.id
        user = UserDetailsModel.objects.filter(id=id)
        return user


class LogoutView(ListAPIView):
   
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        datas = Token.objects.get(user=self.request.user.id)
        datas.delete()
        return Response({
            "Status":True,
            "Data":"Succesfully Logout"
        })


class ChangeStatus(ListAPIView):
    def post(self,request) :
        try:
            id = self.request.data['id']
        except:
            id =""

        if id:
            user = UserDetailsModel.objects.filter(id=id)
            if user.count():
                user = user.first()
                userstatus = user.status
                print("1234567890",userstatus)

                if userstatus == "Active" :
                    user.status = "Block"
                    user.save()
                else:
                    user.status = "Active"
                    user.save()

                
                return Response({"Status" : status.HTTP_200_OK,"Message" : "User Status Changed"})
            else:
                return Response({"Status" : status.HTTP_404_NOT_FOUND,"Message" : "User Does Not Exist"})

        else:
            return Response({"Status" : status.HTTP_400_BAD_REQUEST,"Message" : "Bad Request"})



# class ChangePassword(ListAPIView):
#     def post(self,request):
#         try:      
#             id = self.request.data["id"]
#         except:
#             id = ""   
        
#         if id:
             
           
#             user = UserDetailsModel.objects.filter(id=id)
#             if user.count():
#                 user = user.first()
#             else:
#                 return Response({
#                     "Status" : status.HTTP_404_NOT_FOUND,
#                     "Message" : "User Not Found"
#                 })

#             print(user)

#             if (user.password == self.request.data['oldpassword']):

#                 user.password = make_password(self.request.data['newpassword'])
#                 user.save()
#                 return Response({"Status" : status.HTTP_200_OK,"Message":"Password Succesfully Updated"})
#             else:
#                 return Response({"Status" : status.HTTP_400_BAD_REQUEST,"Message":"Old Password was not correct"})

        

           
        
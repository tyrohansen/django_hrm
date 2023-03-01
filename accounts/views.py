from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from accounts.models import Profile, User
from accounts.serializers import ChangePasswordSerializer, LoginSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, ProfileSerializer, UserRegistrationSerializer, UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'login':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'login':
            return LoginSerializer
        return UserSerializer
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        form = UserRegistrationSerializer(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user = User.objects.create(
                    username=form.validated_data['username'],
                    email=form.validated_data['email'],
                    first_name=form.validated_data['first_name'],
                    last_name=form.validated_data['last_name'],
                )
                user.set_password(form.validated_data['password'])
                user.save()
                Profile.objects.create(
                    user= user,
                )
               
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"message":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    @action(detail=False, methods=['post','get'], serializer_class=LoginSerializer, permission_classes=[AllowAny])
    def login(self, request, pk=None):
        form = LoginSerializer(data=request.data)
        if form.is_valid():
            #login user 
            user = authenticate(request, username=form.validated_data['username'], password=form.validated_data['password'])
            if user and user.is_staff:
                 return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
                
            if user is not None:
                login(request, user)
                auth_data = RefreshToken.for_user(user)
                profile = Profile.objects.filter(user=user).first()
                return Response({
                    'refresh': str(auth_data),
                    'access': str(auth_data.access_token),
                    'profile':ProfileSerializer(profile).data if profile else UserSerializer(user).data
                    }, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'],serializer_class=ChangePasswordSerializer, permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            isLogined = authenticate(request, 
                username=user.username, 
                password=serializer.validated_data['old_password'])
            
            if not isLogined:
                return Response({"message":"Invalid old password"},  status=status.HTTP_400_BAD_REQUEST)
    
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'New password has been set successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'],serializer_class=PasswordResetRequestSerializer, permission_classes=[AllowAny])
    def password_reset_request(self, request, pk=None):
        form = PasswordResetRequestSerializer(data=request.data)
        if form.is_valid():
            # generate token for user
            user = User.objects.filter(email=form.validated_data['email']).first()
            if user:
                token = PasswordResetTokenGenerator().make_token(user=user)
                uid = user.id
                url = f"http://example.com/reset/{uid}/{token}"
                send_mail('You have request for a password reset at kukyooto', 
                    f'Hey {user.first_name},\n\n Please follow the link below to reset your password \n\n {url}', 
                    'example@gmail.com', [user.email], fail_silently=True)
            return Response({"message": "Communication has been sent to prefer recovery method"})

        return Response(form.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def token_validation(self, request):
        token = request.query_params.get('token','0')
        user = User.objects.filter(pk=request.query_params.get('uid')).first()
        if user:
            is_valid_token = PasswordResetTokenGenerator().check_token(user, token)
            if is_valid_token:
                return Response({'message':'Token is valid'}, status=status.HTTP_200_OK)
        return Response({'message':'Invalid token: '}, status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=False, methods=['post'],serializer_class=PasswordResetSerializer, permission_classes=[AllowAny])
    def password_reset(self, request, pk=None):
        form = PasswordResetSerializer(data=request.data)
        if form.is_valid():
            user = User.objects.filter(pk=form.validated_data['user']).first()
            token = PasswordResetTokenGenerator().check_token(user, form.validated_data['token'])
            if token:
                user.set_password(form.validated_data['password'])
                user.save()
                return Response({"details": "Password reset complete"}, status=status.HTTP_200_OK)
            
        return Response(form.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes= (IsAuthenticated,)
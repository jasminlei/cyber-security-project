from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
import logging

logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


# FLAW 5: A09 - Security Logging and Monitoring Failures
# Problem: Only successful logins are logged, failed attempts are NOT logged
# This allows attackers to perform brute-force attacks undetected
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            # only successful logins are logged
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            logger.info(
                f"Successful login: user={user.username}, ip={request.META.get('REMOTE_ADDR')}"
            )

            return Response({"token": token.key, "user": UserSerializer(user).data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FIX: Log both successful and failed login attempts
# class LoginView(ObtainAuthToken):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username', 'unknown')
#         ip_address = request.META.get('REMOTE_ADDR', 'unknown')
#
#         serializer = self.serializer_class(
#             data=request.data, context={"request": request}
#         )
#
#         if serializer.is_valid():
#             user = serializer.validated_data["user"]
#             token, created = Token.objects.get_or_create(user=user)
#
#             logger.info(f"SUCCESS: Login successful - user={user.username}, ip={ip_address}")
#
#             return Response({"token": token.key, "user": UserSerializer(user).data})
#         else:
#             logger.warning(f"FAILED: Login attempt failed - username={username}, ip={ip_address}, errors={serializer.errors}")
#
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

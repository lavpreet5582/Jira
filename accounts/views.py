import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, SignupSerializer, UserSerializer


logger = logging.getLogger(__name__)

class AuthViewset(ViewSet):
    permission_classes = [AllowAny]

    @action(methods=["POST"], detail=False)
    def login(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data["user"]
                refresh = RefreshToken.for_user(user)  # Generate JWT tokens
                logger.info("[Login] User %s Logged In Successfully", user.email)
                return Response({"token": str(refresh.access_token)})
            logger.exception("[Login] Error While Logging In: %s", str(serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("[Login] Error While Logging In: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"], detail=False)
    def whoami(self, request):
        serializer = UserSerializer(request.user)
        logger.info("[WhoAmI] User %s Found Successfully", request.user.email)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False)
    def signup(self, request):
        try:
            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(
                    user
                )  # Generate JWT tokens for newly signed up user
                logger.info("[Signup] User %s Signed Up Successfully", user.email)
                return Response({"token": str(refresh.access_token)})
            logger.exception("[Signup] Error While Signing Up: %s", str(serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("[Signup] Error While Signing Up: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

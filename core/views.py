from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status


from core.serializers import LoginSerializer, PhoneNumberSerializer, OTPSerializer, SetPasswordSerializer, UserSerializer

from core.models import OTP


User = get_user_model()


class OTPRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        return Response({"message": "Enter your phone number."})

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        user, created = User.objects.get_or_create(phone_number=phone_number)

        if not created and user.is_active:
            return Response(
                {"message": "User already exists. Proceed to login"},
                status=status.HTTP_200_OK
            )

        otp = OTP.objects.create(user=user)

        print("Otp code is sent to user", otp.code)

        return Response(
            {"message": f"Verification code sent to {phone_number}. Proceed to OTP verification"},
            status=status.HTTP_201_CREATED
        )


class OTPVerificationView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        return Response(
            {"message": "Enter your Phone number and OTP code."},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp']

        try:
            user = User.objects.get(phone_number=phone_number)
            otp = OTP.objects.get(user=user, code=otp_code)

            if not otp.is_valid():
                return Response(
                    {"message": "OTP has expired."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.is_active = True
            user.save()
            token = RefreshToken.for_user(user)
            otp.delete()

            return Response(
                {
                    "message": "OTP verified successfully. You may proceed to complete your profile",
                    "refresh": str(token),
                    "access": str(token.access_token)
                },
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        except OTP.DoesNotExist:
            return Response(
                {"message": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({"message": f"{e!r}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(GenericViewSet):

    serializer_class = UserSerializer

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        elif request.method == "PATCH":
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class SetPasswordView(APIView):

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(phone_number=phone_number)
            if not user.is_active:
                return Response(
                    {"message": "User is not active."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(make_password(password))
            user.save()

            return Response(
                {"message": "Password set successfully."},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response({"message": f"{e!r}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        try:
            user = User.objects.get(phone_number=phone_number)
            user.check_password(password)

            if user is None:
                raise AuthenticationFailed("Invalid credentials")

            token = RefreshToken.for_user(user)
            return Response({
                "refresh": str(token),
                "access": str(token.access_token),
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User with this credentails does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": f"{e!r}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

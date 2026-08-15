from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": "رمز عبور فعلی نادرست است."}, status=400)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "رمز عبور با موفقیت تغییر کرد."})


class PasswordResetRequestView(APIView):
    """درخواست بازیابی رمز عبور - لینک حاوی uid و token در کنسول ایمیل نمایش داده می‌شود."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email__iexact=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_RESET_PASSWORD_URL}/{uid}/{token}"
            send_mail(
                subject="بازیابی رمز عبور فروشگاه یاشیل آرت",
                message=f"برای بازیابی رمز عبور خود روی لینک زیر کلیک کنید:\n{reset_link}",
                from_email="no-reply@kaavan-shop.local",
                recipient_list=[email],
                fail_silently=True,
            )
        # همیشه پاسخ یکسان می‌دهیم تا وجود/عدم وجود ایمیل قابل شناسایی نباشد
        return Response({"detail": "در صورت وجود این ایمیل، لینک بازیابی ارسال شد."})


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            uid = force_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"detail": "لینک بازیابی نامعتبر است."}, status=400)

        if not default_token_generator.check_token(user, data["token"]):
            return Response({"detail": "لینک بازیابی نامعتبر یا منقضی شده است."}, status=400)

        user.set_password(data["new_password"])
        user.save()
        return Response({"detail": "رمز عبور با موفقیت بازنشانی شد."})

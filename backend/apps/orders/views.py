from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from apps.access.permissions import IsAdminWithModelPerm

from .models import Order
from .serializers import CheckoutSerializer, OrderSerializer, OrderStatusUpdateSerializer


class CheckoutView(generics.CreateAPIView):
    """ثبت سفارش نهایی از سبد خرید کاربر لاگین‌کرده."""

    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class MyOrdersViewSet(viewsets.ReadOnlyModelViewSet):
    """سفارش‌های کاربر جاری (برای صفحه «سفارش‌های من»)."""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")


class AdminOrderViewSet(viewsets.ModelViewSet):
    """مدیریت همه سفارش‌ها - فقط ادمین (پنل ادمین)."""

    queryset = Order.objects.all().prefetch_related("items").select_related("user")
    serializer_class = OrderSerializer
    permission_classes = [IsAdminWithModelPerm]
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == "partial_update":
            return OrderStatusUpdateSerializer
        return OrderSerializer

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        instance = self.get_object()

        if instance.status == Order.Status.PAID:
            from apps.accounting.services import ensure_income_transaction

            ensure_income_transaction(instance, request.user)

        return Response(OrderSerializer(instance).data)
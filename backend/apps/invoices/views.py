import logging

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.access.permissions import IsAdminWithModelPerm

from .models import Invoice
from .serializers import (
    InvoiceArchiveSerializer,
    InvoiceListSerializer,
    InvoiceNoteUpdateSerializer,
    InvoiceSerializer,
    InvoiceStatusUpdateSerializer,
)
from .services import generate_invoice_pdf, send_invoice_email

logger = logging.getLogger(__name__)


class AllowTokenFromQueryOrHeader(permissions.BasePermission):
    """احراز هویت از هدر Authorization یا query string ?token=..."""

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        token = request.query_params.get("token")
        if not token:
            return False

        try:
            jwt_auth = JWTAuthentication()
            validated = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated)
            request.user = user
            return True
        except (InvalidToken, TokenError, Exception):
            return False


class MyInvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    فاکتورهای کاربر جاری.
    """

    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(
            user=self.request.user
        ).select_related("order").prefetch_related("items")

    def get_serializer_class(self):
        if self.action == "list":
            return InvoiceListSerializer
        return InvoiceSerializer

    @action(
        detail=True,
        methods=["get"],
        url_path="download-pdf",
        permission_classes=[AllowTokenFromQueryOrHeader],
    )
    def download_pdf(self, request, pk=None):
        """دانلود PDF فاکتور — نمایش صفحه HTML چاپ‌پذیر"""
        invoice = self.get_object()
        items = invoice.items.all()
        html_string = render_to_string(
            "invoices/print_invoice.html",
            {"invoice": invoice, "items": items},
        )
        return HttpResponse(html_string)

    @action(
        detail=True,
        methods=["get"],
        url_path="raw-pdf",
        permission_classes=[AllowTokenFromQueryOrHeader],
    )
    def raw_pdf(self, request, pk=None):
        """دانلود فایل PDF خام"""
        invoice = self.get_object()
        try:
            pdf_content = generate_invoice_pdf(invoice)
        except Exception as e:
            logger.error("PDF error for %s: %s", invoice.invoice_number, e, exc_info=True)
            pdf_content = None

        if not pdf_content:
            return Response(
                {"error": "خطا در تولید PDF."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response = HttpResponse(pdf_content, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{invoice.invoice_number}.pdf"'
        )
        return response


class AdminInvoiceViewSet(viewsets.ModelViewSet):
    """
    مدیریت فاکتورها توسط ادمین.
    """

    queryset = Invoice.objects.all().select_related("order", "user").prefetch_related("items")
    permission_classes = [IsAdminWithModelPerm]
    http_method_names = ["get", "patch", "delete", "head", "options", "post"]

    def get_serializer_class(self):
        if self.action == "list":
            return InvoiceListSerializer
        if self.action == "partial_update":
            return InvoiceStatusUpdateSerializer
        return InvoiceSerializer

    @action(detail=True, methods=["post"], url_path="archive")
    def archive_toggle(self, request, pk=None):
        invoice = self.get_object()
        serializer = InvoiceArchiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["archive"]:
            invoice.archive()
        else:
            invoice.unarchive()
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["post"], url_path="send-email")
    def send_email(self, request, pk=None):
        invoice = self.get_object()
        if not invoice.buyer_email:
            return Response(
                {"error": "ایمیل خریدار ثبت نشده است."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        success = send_invoice_email(invoice, request)
        if success:
            return Response({"message": "ایمیل فاکتور با موفقیت ارسال شد."})
        return Response(
            {"error": "خطا در ارسال ایمیل."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="download-pdf",
        permission_classes=[AllowTokenFromQueryOrHeader],
    )
    def download_pdf(self, request, pk=None):
        """دانلود PDF فاکتور — نمایش صفحه HTML چاپ‌پذیر"""
        invoice = self.get_object()
        items = invoice.items.all()
        html_string = render_to_string(
            "invoices/print_invoice.html",
            {"invoice": invoice, "items": items},
        )
        return HttpResponse(html_string)

    @action(
        detail=True,
        methods=["get"],
        url_path="raw-pdf",
        permission_classes=[AllowTokenFromQueryOrHeader],
    )
    def raw_pdf(self, request, pk=None):
        """دانلود فایل PDF خام"""
        invoice = self.get_object()
        try:
            pdf_content = generate_invoice_pdf(invoice)
        except Exception as e:
            logger.error("Admin PDF error for %s: %s", invoice.invoice_number, e, exc_info=True)
            pdf_content = None
        if not pdf_content:
            return Response(
                {"error": "خطا در تولید PDF."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response = HttpResponse(pdf_content, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{invoice.invoice_number}.pdf"'
        )
        return response
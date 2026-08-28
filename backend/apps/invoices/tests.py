from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.orders.models import Order, OrderItem

from .models import Invoice
from .services import create_invoice_for_order


class InvoiceServiceTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="invoice-test",
            password="test-password",
        )
        self.order = Order.objects.create(
            user=self.user,
            status=Order.Status.PAID,
            full_name="کاربر تست",
            phone_number="09120000000",
            address="آدرس تست",
            postal_code="1234567890",
            total_price=300000,
        )
        OrderItem.objects.create(
            order=self.order,
            product=None,
            product_name="محصول تست",
            variant_label="",
            unit_price=300000,
            quantity=1,
        )

    def test_invoice_created_once(self):
        first = create_invoice_for_order(self.order)
        second = create_invoice_for_order(self.order)

        self.assertIsNotNone(first)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(
            Invoice.objects.filter(order=self.order).count(),
            1,
        )
        self.assertTrue(first.invoice_number.startswith("YA-"))

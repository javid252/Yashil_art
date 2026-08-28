import logging
import os

from django.utils import timezone

from .models import Invoice, InvoiceItem

logger = logging.getLogger(__name__)


def _reshape_persian(text):
    """
    شکل‌دهی صحیح حروف فارسی/عربی برای PDF.
    حروف فارسی باید به شکل ارتباطی (connected) تبدیل شوند
    و جهت متن (RTL) رعایت شود.
    """
    if not text:
        return text

    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        # شکل‌دهی حروف ارتباطی
        reshaped = arabic_reshaper.reshape(str(text))
        # اعمال الگوریتم bidi برای جهت درست متن
        bidi_text = get_display(reshaped)
        return bidi_text
    except ImportError:
        return str(text)
    except Exception:
        return str(text)


def _find_pesian_font():
    """
    پیدا کردن فونت فارسی مناسب در سیستم.
    اولویت با فونت‌های رایج فارسی است.
    """
    font_search_paths = [
        # ویندوز
        r"C:\Windows\Fonts\Tahoma.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
        r"C:\Windows\Fonts\B-NAZANIN.TTF",
        r"C:\Windows\Fonts\b-nazanin.ttf",
        r"C:\Windows\Fonts\IRANSans.ttf",
        r"C:\Windows\Fonts\iransans.ttf",
        r"C:\Windows\Fonts\Vazirmatn-Regular.ttf",
        r"C:\Windows\Fonts\vazirmatn-regular.ttf",
        # لینوکس
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/tahoma.ttf",
        "/usr/share/fonts/TTF/tahoma.ttf",
        # مک
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]

    for font_path in font_search_paths:
        if os.path.exists(font_path):
            return font_path

    return None


def generate_invoice_from_order(order, force=False):
    """
    صدور خودکار فاکتور از یک سفارش.
    """
    existing = Invoice.objects.filter(order=order).first()
    if existing and not force:
        return existing, False

    if existing and force:
        existing.delete()

    invoice = Invoice.objects.create(
        order=order,
        user=order.user,
        buyer_full_name=order.full_name,
        buyer_phone=order.phone_number,
        buyer_address=order.address,
        buyer_postal_code=order.postal_code,
        status=Invoice.Status.DRAFT,
    )

    for order_item in order.items.select_related("product", "variant").all():
        InvoiceItem.objects.create(
            invoice=invoice,
            product=order_item.product,
            product_name=order_item.product_name,
            variant_label=order_item.variant_label,
            unit_price=order_item.unit_price,
            quantity=order_item.quantity,
        )

    invoice.recalculate_totals()
    invoice.mark_issued()

    return invoice, True


def send_invoice_email(invoice, request=None):
    """
    ارسال ایمیل فاکتور به خریدار.
    """
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags

    if not invoice.buyer_email:
        return False

    html_content = render_to_string(
        "invoices/email_invoice.html",
        {"invoice": invoice, "items": invoice.items.all()},
    )
    text_content = strip_tags(html_content)

    subject = f"فاکتور خرید {invoice.invoice_number} - فروشگاه یاشیل آرت"

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=None,
        to=[invoice.buyer_email],
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        pdf_content = generate_invoice_pdf(invoice)
        if pdf_content:
            msg.attach(
                f"{invoice.invoice_number}.pdf",
                pdf_content,
                "application/pdf",
            )
    except Exception:
        pass

    msg.send()

    invoice.email_sent = True
    invoice.email_sent_at = timezone.now()
    invoice.save(update_fields=["email_sent", "email_sent_at", "updated_at"])

    return True


def generate_invoice_pdf(invoice):
    """
    تولید PDF فاکتور با فونت فارسی صحیح.
    از arabic_reshaper و bidi برای شکل‌دهی درست حروف استفاده می‌شود.
    """
    try:
        from io import BytesIO

        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import (
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
            Paragraph,
        )

        # --- ثبت فونت ---
        font_path = _find_pesian_font()
        font_name = "Helvetica"  # fallback

        if font_path:
            try:
                pdfmetrics.registerFont(TTFont("PersianFont", font_path))
                font_name = "PersianFont"
                logger.info("Registered Persian font: %s", font_path)
            except Exception as e:
                logger.warning("Failed to register font %s: %s", font_path, e)

        # --- ساخت PDF ---
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            rightMargin=15 * mm, leftMargin=15 * mm,
            topMargin=15 * mm, bottomMargin=15 * mm,
        )

        styles = getSampleStyleSheet()

        # استایل‌ها (همه از TA_RIGHT برای RTL)
        style_badge = ParagraphStyle(
            "Badge", parent=styles["Heading2"],
            fontName=font_name, fontSize=14, textColor=colors.white,
            alignment=TA_CENTER, spaceAfter=6,
        )
        style_normal = ParagraphStyle(
            "NormalFA", parent=styles["Normal"],
            fontName=font_name, fontSize=10, alignment=TA_RIGHT,
        )
        style_right = ParagraphStyle(
            "RightFA", parent=styles["Normal"],
            fontName=font_name, fontSize=10, alignment=TA_RIGHT,
        )
        style_left = ParagraphStyle(
            "LeftFA", parent=styles["Normal"],
            fontName=font_name, fontSize=10, alignment=TA_LEFT,
        )
        style_header_cell = ParagraphStyle(
            "HeaderCell", parent=styles["Normal"],
            fontName=font_name, fontSize=9, textColor=colors.white,
            alignment=TA_CENTER,
        )
        style_cell = ParagraphStyle(
            "Cell", parent=styles["Normal"],
            fontName=font_name, fontSize=9, alignment=TA_CENTER,
        )
        style_cell_right = ParagraphStyle(
            "CellRight", parent=styles["Normal"],
            fontName=font_name, fontSize=9, alignment=TA_RIGHT,
        )
        style_total = ParagraphStyle(
            "Total", parent=styles["Normal"],
            fontName=font_name, fontSize=13, textColor=colors.white,
            alignment=TA_LEFT,
        )
        style_total_label = ParagraphStyle(
            "TotalLabel", parent=styles["Normal"],
            fontName=font_name, fontSize=11, textColor=colors.white,
            alignment=TA_RIGHT,
        )
        style_footer = ParagraphStyle(
            "Footer", parent=styles["Normal"],
            fontName=font_name, fontSize=9, textColor=colors.grey,
            alignment=TA_CENTER, spaceBefore=10,
        )

        elements = []

        # --- helper for safe text ---
        def P(text, style):
            """ایجاد Paragraph با متن reshape شده فارسی"""
            return Paragraph(_reshape_persian(text), style)

        # --- هدر ---
        issued_date = invoice.issued_at.strftime('%Y/%m/%d %H:%M') if invoice.issued_at else '-'
        header_data = [[
            P(f"<b>{invoice.invoice_number}</b>", style_left),
            P(_reshape_persian("یاشیل آرت"), style_right),
        ]]
        header_table = Table(header_data, colWidths=[doc.width * 0.45, doc.width * 0.55])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LINEBELOW', (0, 0), (-1, 0), 3, colors.HexColor("#16a085")),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 10))

        # --- بج فاکتور ---
        badge_data = [[
            P(_reshape_persian("فاکتور فروش"), style_badge),
        ]]
        badge_table = Table(badge_data, colWidths=[doc.width])
        badge_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#16a085")),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('TOPPADDING', (0, 0), (0, 0), 8),
            ('BOTTOMPADDING', (0, 0), (0, 0), 8),
        ]))
        elements.append(badge_table)
        elements.append(Spacer(1, 10))

        # --- اطلاعات خریدار ---
        buyer_lines = [
            _reshape_persian("اطلاعات خریدار"),
            f"{_reshape_persian('نام')}: {invoice.buyer_full_name}",
            f"{_reshape_persian('تلفن')}: {invoice.buyer_phone or '-'}",
            f"{_reshape_persian('ایمیل')}: {invoice.buyer_email or '-'}",
            f"{_reshape_persian('آدرس')}: {invoice.buyer_address or '-'}",
            f"{_reshape_persian('کد پستی')}: {invoice.buyer_postal_code or '-'}",
        ]
        buyer_info = "<br/>".join(buyer_lines)

        order_date = invoice.order.created_at.strftime('%Y/%m/%d %H:%M') if invoice.order.created_at else '-'
        status_lines = [
            _reshape_persian("وضعیت فاکتور"),
            f"{_reshape_persian('شماره سفارش')}: #{invoice.order_id}",
            f"{_reshape_persian('تاریخ ثبت')}: {order_date}",
            f"{_reshape_persian('وضعیت')}: {invoice.get_status_display()}",
        ]
        if invoice.email_sent:
            status_lines.append(
                f"{_reshape_persian('ارسال ایمیل')}: {_reshape_persian('بله')}"
            )
        status_info = "<br/>".join(status_lines)

        info_data = [[
            P(buyer_info, style_right),
            P(status_info, style_right),
        ]]
        info_table = Table(info_data, colWidths=[doc.width * 0.5, doc.width * 0.5])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#f8f9fa")),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#f8f9fa")),
            ('BOX', (0, 0), (0, 0), 1, colors.HexColor("#e9ecef")),
            ('BOX', (1, 0), (1, 0), 1, colors.HexColor("#e9ecef")),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 12))

        # --- جدول آیتم‌ها ---
        table_data = [[
            P(_reshape_persian("#"), style_header_cell),
            P(_reshape_persian("نام محصول"), style_header_cell),
            P(_reshape_persian("مشخصات"), style_header_cell),
            P(_reshape_persian("قیمت واحد"), style_header_cell),
            P(_reshape_persian("تعداد"), style_header_cell),
            P(_reshape_persian("جمع ردیف"), style_header_cell),
        ]]

        for idx, item in enumerate(invoice.items.all(), 1):
            table_data.append([
                P(str(idx), style_cell),
                P(_reshape_persian(item.product_name), style_cell_right),
                P(_reshape_persian(item.variant_label or '-'), style_cell),
                P(f"{int(item.unit_price):,} {_reshape_persian('تومان')}", style_cell),
                P(str(item.quantity), style_cell),
                P(f"{int(item.line_total_after_discount):,} {_reshape_persian('تومان')}", style_cell),
            ])

        items_table = Table(
            table_data,
            colWidths=[
                doc.width * 0.05, doc.width * 0.30, doc.width * 0.15,
                doc.width * 0.18, doc.width * 0.10, doc.width * 0.22,
            ],
        )
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#16a085")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e9ecef")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 12))

        # --- خلاصه مالی ---
        summary_data = []
        summary_data.append([
            P(_reshape_persian("جمع آیتم‌ها:"), style_right),
            P(f"{int(invoice.subtotal):,} {_reshape_persian('تومان')}", style_left),
        ])
        if invoice.discount_total > 0:
            summary_data.append([
                P(_reshape_persian("تخفیف:"), style_right),
                P(f"-{int(invoice.discount_total):,} {_reshape_persian('تومان')}", style_left),
            ])
        if invoice.tax_total > 0:
            summary_data.append([
                P(_reshape_persian("مالیات:"), style_right),
                P(f"{int(invoice.tax_total):,} {_reshape_persian('تومان')}", style_left),
            ])
        summary_data.append([
            P(_reshape_persian("مبلغ نهایی:"), style_total_label),
            P(f"{invoice.formatted_grand_total} {_reshape_persian('تومان')}", style_total),
        ])

        summary_table = Table(summary_data, colWidths=[doc.width * 0.5, doc.width * 0.5])
        summary_style = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor("#dee2e6")),
        ]
        summary_style.append(('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#16a085")))
        summary_style.append(('TOPPADDING', (0, -1), (-1, -1), 10))
        summary_style.append(('BOTTOMPADDING', (0, -1), (-1, -1), 10))
        summary_table.setStyle(TableStyle(summary_style))
        elements.append(summary_table)

        # --- یادداشت ---
        if invoice.notes:
            elements.append(Spacer(1, 10))
            notes_data = [[P(
                _reshape_persian(f"یادداشت: {invoice.notes}"),
                ParagraphStyle("Notes", parent=style_normal, fontSize=9, textColor=colors.HexColor("#856404")),
            )]]
            notes_table = Table(notes_data, colWidths=[doc.width])
            notes_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#fff3cd")),
                ('BOX', (0, 0), (0, 0), 1, colors.HexColor("#ffc107")),
                ('TOPPADDING', (0, 0), (0, 0), 8),
                ('BOTTOMPADDING', (0, 0), (0, 0), 8),
                ('LEFTPADDING', (0, 0), (0, 0), 10),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
            ]))
            elements.append(notes_table)

        # --- فوتر ---
        elements.append(Spacer(1, 15))
        elements.append(P(
            _reshape_persian("این فاکتور به‌صورت خودکار توسط سامانه فروشگاه یاشیل آرت صادر شده است."),
            style_footer,
        ))
        elements.append(P(
            _reshape_persian("یاشیل آرت | yashilartshop.ir"),
            style_footer,
        ))

        # --- ساخت PDF ---
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

    except ImportError as e:
        logger.warning("Missing dependency for PDF: %s", e)
        return None
    except Exception as e:
        logger.error("PDF generation failed for invoice %s: %s", invoice.invoice_number, e, exc_info=True)
        import traceback
        traceback.print_exc()
        raise
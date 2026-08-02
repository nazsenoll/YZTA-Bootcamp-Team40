"""
SMTP uzerinden e-posta dogrulama kodu gonderen basit modul.
Ucuncu parti bagimlilik gerektirmez (smtplib standart kutuphanededir).

.env'de gerekli degiskenler:
  SMTP_HOST      -- ör. smtp.gmail.com
  SMTP_PORT      -- ör. 587
  SMTP_USERNAME  -- gonderen hesabin adresi
  SMTP_PASSWORD  -- gonderen hesabin sifresi / uygulama sifresi
  SMTP_FROM      -- (opsiyonel) gorunecek gonderen adresi, yoksa SMTP_USERNAME kullanilir
  SMTP_USE_TLS   -- "true"/"false" (varsayilan true)

Not: Gmail kullaniyorsan normal hesap sifresi degil, Google hesabinda
olusturulan bir "Uygulama Sifresi" (App Password) gerekir.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587") or "587")
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_FROM = os.environ.get("SMTP_FROM", "") or SMTP_USERNAME
SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").strip().lower() != "false"


class MailError(Exception):
    pass


def is_configured() -> bool:
    return bool(SMTP_HOST and SMTP_USERNAME and SMTP_PASSWORD)


def send_verification_email(to_email: str, code: str) -> None:
    if not is_configured():
        raise MailError(
            "SMTP ayarlari .env dosyasinda eksik "
            "(SMTP_HOST / SMTP_USERNAME / SMTP_PASSWORD gerekli)."
        )

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = "AskQL - E-posta Dogrulama Kodu"

    body = (
        "Merhaba,\n\n"
        "AskQL hesabinizi dogrulamak icin asagidaki kodu kullanin:\n\n"
        f"    {code}\n\n"
        "Bu kod 15 dakika icinde gecerliligini yitirecektir.\n\n"
        "Bu istegi siz yapmadiysaniz bu e-postayi yok sayabilirsiniz.\n"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            if SMTP_USE_TLS:
                server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise MailError(f"E-posta gonderilemedi: {e}")


TITLE_LABELS = {"yonetici": "Yönetici", "mudur": "Müdür", "calisan": "Çalışan"}


def send_employee_invite_email(to_email: str, company_name: str, title: str, temp_password: str) -> None:
    """Yonetici tarafindan eklenen bir calisana gecici sifresini gonderir."""
    if not is_configured():
        raise MailError(
            "SMTP ayarlari .env dosyasinda eksik "
            "(SMTP_HOST / SMTP_USERNAME / SMTP_PASSWORD gerekli)."
        )

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = f"AskQL - {company_name} hesabınız oluşturuldu"

    title_label = TITLE_LABELS.get(title, title)
    body = (
        "Merhaba,\n\n"
        f"{company_name} icin AskQL hesabiniz olusturuldu. Unvaniniz: {title_label}.\n\n"
        f"Giris e-postaniz: {to_email}\n"
        f"Gecici sifreniz: {temp_password}\n\n"
        "Ilk girisinizde bu sifreyi degistirmeniz istenecektir.\n"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            if SMTP_USE_TLS:
                server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise MailError(f"E-posta gonderilemedi: {e}")
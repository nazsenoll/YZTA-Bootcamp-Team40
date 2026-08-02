"""
Uygulama girisi icin sirket + kullanici kaydi katmani (Supabase/Postgres).

Model:
  companies(id, name, sql_server, sql_database, sql_username, sql_password, created_at)
  users(id, email, password_hash, company_id, title, verified, must_change_password,
        verification_code, code_expires_at, created_at)
"""

import os
import re
import secrets
import string
from datetime import datetime, timedelta, timezone

from supabase import Client, create_client
from werkzeug.security import check_password_hash, generate_password_hash

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

CODE_TTL_MINUTES = 15
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
VALID_TITLES = {"yonetici", "mudur", "calisan"}

_client = None


class UserError(Exception):
    pass


def _get_client():
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise UserError(
                "Supabase baglanti bilgileri eksik "
                "(.env icinde SUPABASE_URL / SUPABASE_SERVICE_KEY gerekli)."
            )
        _client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return _client


def init_db() -> None:
    try:
        client = _get_client()
        client.table("users").select("id").limit(1).execute()
        client.table("companies").select("id").limit(1).execute()
    except UserError:
        raise
    except Exception as e:
        raise UserError(
            f"Supabase tablolarina erisilemedi: {e}. "
            f"supabase_setup_v2.sql scriptini Supabase SQL Editor'da calistirdigindan emin ol."
        )


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match((email or "").strip()))


def _generate_code() -> str:
    return "".join(secrets.choice(string.digits) for _ in range(6))


def _generate_temp_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(10))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _expiry_iso() -> str:
    return (datetime.now(timezone.utc) + timedelta(minutes=CODE_TTL_MINUTES)).isoformat()


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def register_company(company_name: str, email: str, password: str) -> str:
    company_name = (company_name or "").strip()
    email = (email or "").strip().lower()

    if not company_name:
        raise UserError("Sirket adi gerekli.")
    if not is_valid_email(email):
        raise UserError("Gecerli bir e-posta adresi gir.")
    if len(password or "") < 6:
        raise UserError("Sifre en az 6 karakter olmali.")

    client = _get_client()
    existing = client.table("users").select("*").eq("email", email).execute()
    rows = existing.data or []

    code = _generate_code()
    expires_at = _expiry_iso()
    pw_hash = generate_password_hash(password)

    if not rows:
        company_res = client.table("companies").insert({
            "name": company_name,
            "created_at": _now_iso(),
        }).execute()
        company_id = company_res.data[0]["id"]
        client.table("users").insert({
            "email": email,
            "password_hash": pw_hash,
            "company_id": company_id,
            "title": "yonetici",
            "verified": False,
            "must_change_password": False,
            "verification_code": code,
            "code_expires_at": expires_at,
            "created_at": _now_iso(),
        }).execute()
    else:
        row = rows[0]
        if row["verified"]:
            raise UserError("Bu e-posta zaten kayitli ve dogrulanmis. Giris yapmayi dene.")
        client.table("companies").update({"name": company_name}).eq("id", row["company_id"]).execute()
        client.table("users").update({
            "password_hash": pw_hash,
            "verification_code": code,
            "code_expires_at": expires_at,
        }).eq("email", email).execute()

    return code


def resend_code(email: str) -> str:
    email = (email or "").strip().lower()
    client = _get_client()
    existing = client.table("users").select("*").eq("email", email).execute()
    rows = existing.data or []

    if not rows:
        raise UserError("Bu e-posta ile kayit bulunamadi.")
    if rows[0]["verified"]:
        raise UserError("Bu hesap zaten dogrulanmis.")

    code = _generate_code()
    expires_at = _expiry_iso()
    client.table("users").update({
        "verification_code": code,
        "code_expires_at": expires_at,
    }).eq("email", email).execute()

    return code


def verify_code(email: str, code: str) -> dict:
    email = (email or "").strip().lower()
    code = (code or "").strip()
    client = _get_client()
    existing = client.table("users").select("*").eq("email", email).execute()
    rows = existing.data or []

    if not rows:
        raise UserError("Bu e-posta ile kayit bulunamadi.")
    row = rows[0]

    if row["verified"]:
        raise UserError("Bu hesap zaten dogrulanmis.")
    if not row.get("verification_code") or row["verification_code"] != code:
        raise UserError("Dogrulama kodu hatali.")
    if not row.get("code_expires_at") or _parse_dt(row["code_expires_at"]) < datetime.now(timezone.utc):
        raise UserError("Dogrulama kodunun suresi dolmus. Yeni kod iste.")

    client.table("users").update({
        "verified": True,
        "verification_code": None,
        "code_expires_at": None,
    }).eq("email", email).execute()

    row["verified"] = True
    return row


def check_login(email: str, password: str) -> dict:
    email = (email or "").strip().lower()
    client = _get_client()
    existing = client.table("users").select("*").eq("email", email).execute()
    rows = existing.data or []

    if not rows or not check_password_hash(rows[0]["password_hash"], password or ""):
        raise UserError("E-posta veya sifre hatali.")
    if not rows[0]["verified"]:
        raise UserError("Hesabin dogrulanmamis. E-postana gelen kodu gir.")
    return rows[0]


def change_password(email: str, current_password: str, new_password: str) -> None:
    email = (email or "").strip().lower()
    if len(new_password or "") < 6:
        raise UserError("Yeni sifre en az 6 karakter olmali.")

    client = _get_client()
    existing = client.table("users").select("*").eq("email", email).execute()
    rows = existing.data or []
    if not rows or not check_password_hash(rows[0]["password_hash"], current_password or ""):
        raise UserError("Mevcut sifre hatali.")

    client.table("users").update({
        "password_hash": generate_password_hash(new_password),
        "must_change_password": False,
    }).eq("email", email).execute()


def get_company(company_id) -> dict:
    client = _get_client()
    res = client.table("companies").select("*").eq("id", company_id).limit(1).execute()
    rows = res.data or []
    if not rows:
        raise UserError("Sirket bulunamadi.")
    return rows[0]


def save_company_connection(company_id, server: str, database: str, username: str, password: str) -> None:
    client = _get_client()
    client.table("companies").update({
        "sql_server": server,
        "sql_database": database,
        "sql_username": username,
        "sql_password": password,
    }).eq("id", company_id).execute()


def list_employees(company_id) -> list:
    client = _get_client()
    res = (
        client.table("users")
        .select("email,title,verified,must_change_password,created_at")
        .eq("company_id", company_id)
        .order("created_at")
        .execute()
    )
    return res.data or []


def add_employee(company_id, email: str, title: str) -> str:
    email = (email or "").strip().lower()
    title = (title or "").strip().lower()

    if not is_valid_email(email):
        raise UserError("Gecerli bir e-posta adresi gir.")
    if title not in VALID_TITLES:
        raise UserError("Gecersiz unvan (yonetici / mudur / calisan olmali).")

    client = _get_client()
    existing = client.table("users").select("id").eq("email", email).execute()
    if existing.data:
        raise UserError("Bu e-posta zaten kayitli.")

    temp_password = _generate_temp_password()
    client.table("users").insert({
        "email": email,
        "password_hash": generate_password_hash(temp_password),
        "company_id": company_id,
        "title": title,
        "verified": True,
        "must_change_password": True,
        "verification_code": None,
        "code_expires_at": None,
        "created_at": _now_iso(),
    }).execute()

    return temp_password
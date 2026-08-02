import io
import os
import re
from functools import wraps

from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta

from flask import Flask, jsonify, render_template, request, session, send_file

import chart
import db
import llm
import mailer
import report
import users_db

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-key")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

MAX_HISTORY = 5

# Uygulama girisi artik "sirket + calisanlari" modeline dayanir (bkz.
# users_db.py). Ilk kayit bir sirket olusturur (kisi = yonetici), yonetici
# sonradan "Calisan Ekle" ile diger kullanicilari (mudur/calisan unvaniyla)
# ekler. Kullanici verisi Supabase'de (Postgres) tutulur. Bu, veritabani
# baglantisindan (SQL Server kimlik bilgileri) tamamen AYRI bir kimlik
# dogrulama katmanidir; ikisi birbirine karismaz.
try:
    users_db.init_db()
except users_db.UserError as e:
    print(f"[UYARI] Kullanici veritabani (Supabase) hazir degil: {e}")


def login_required(view):
    """Bu decorator ile isaretlenen route'lar, once /api/login ile giris
    yapilmis olmasini sart kosar. Veritabani baglantisindan bagimsizdir."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("authenticated"):
            return jsonify({"ok": False, "error": "Once giris yapmalisin."}), 401
        return view(*args, **kwargs)
    return wrapped


def yonetici_required(view):
    """Sadece 'yonetici' unvanina sahip kullanicilarin erisebilecegi route'lar icin.
    login_required ile birlikte kullanilmali (bu decorator session["role"]'un
    zaten set edilmis oldugunu varsayar)."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "yonetici":
            return jsonify({"ok": False, "error": "Bu islem sadece yonetici unvanina aciktir."}), 403
        return view(*args, **kwargs)
    return wrapped


def _login_session(user: dict) -> None:
    """Dogrulama/giris basarili olduktan sonra session'i kullanicinin
    sirket/unvan bilgisiyle doldurur. Rol (yetki) artik SQL Server izninden
    degil, buradaki 'title' alanindan gelir."""
    session["authenticated"] = True
    session["email"] = user["email"]
    session["company_id"] = user["company_id"]
    session["role"] = user.get("title", "calisan")
    session["must_change_password"] = bool(user.get("must_change_password"))
    try:
        company = users_db.get_company(user["company_id"])
        session["company_name"] = company.get("name", "")
    except users_db.UserError:
        session["company_name"] = ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/register", methods=["POST"])
def api_register():
    """Yeni SIRKET kaydi olusturur (kayit yapan kisi otomatik 'yonetici' unvanini
    alir) ve e-postaya 6 haneli dogrulama kodu gonderir."""
    data = request.get_json(force=True)
    company_name = (data.get("company") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    password_confirm = data.get("password_confirm") or ""

    if not company_name or not email or not password:
        return jsonify({"ok": False, "error": "Sirket adi, e-posta ve sifre gerekli."}), 400
    if password != password_confirm:
        return jsonify({"ok": False, "error": "Sifreler eslesmiyor."}), 400

    try:
        code = users_db.register_company(company_name, email, password)
    except users_db.UserError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    try:
        mailer.send_verification_email(email, code)
    except mailer.MailError as e:
        return jsonify({
            "ok": False,
            "error": f"Kayit olusturuldu ama dogrulama e-postasi gonderilemedi: {e}",
            "needs_verification": True,
        }), 502

    return jsonify({"ok": True, "email": email, "needs_verification": True})


@app.route("/api/verify", methods=["POST"])
def api_verify():
    """Kayit sirasinda e-postaya gonderilen 6 haneli kodu dogrular.
    Basarili olursa kullaniciyi otomatik olarak oturum acmis sayar."""
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    code = (data.get("code") or "").strip()

    if not email or not code:
        return jsonify({"ok": False, "error": "E-posta ve kod gerekli."}), 400

    try:
        user = users_db.verify_code(email, code)
    except users_db.UserError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    _login_session(user)
    return jsonify({"ok": True, "email": email, "must_change_password": session["must_change_password"]})


@app.route("/api/resend_code", methods=["POST"])
def api_resend_code():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    if not email:
        return jsonify({"ok": False, "error": "E-posta gerekli."}), 400

    try:
        code = users_db.resend_code(email)
    except users_db.UserError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    try:
        mailer.send_verification_email(email, code)
    except mailer.MailError as e:
        return jsonify({"ok": False, "error": str(e)}), 502

    return jsonify({"ok": True})


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"ok": False, "error": "E-posta ve sifre gerekli."}), 400

    try:
        user = users_db.check_login(email, password)
    except users_db.UserError as e:
        needs_verification = "dogrulanmamis" in str(e)
        return jsonify({"ok": False, "error": str(e), "needs_verification": needs_verification}), 401

    remember = bool(data.get("remember"))
    session.permanent = remember

    _login_session(user)
    return jsonify({"ok": True, "email": email, "must_change_password": session["must_change_password"]})


@app.route("/api/change_password", methods=["POST"])
@login_required
def api_change_password():
    """must_change_password=True olan (yonetici tarafindan eklenmis) kullanicilar
    ilk giriste, veya herhangi bir kullanici istedigi zaman sifresini degistirebilir."""
    data = request.get_json(force=True)
    current_password = data.get("current_password") or ""
    new_password = data.get("new_password") or ""
    new_password_confirm = data.get("new_password_confirm") or ""

    if new_password != new_password_confirm:
        return jsonify({"ok": False, "error": "Yeni sifreler eslesmiyor."}), 400

    try:
        users_db.change_password(session["email"], current_password, new_password)
    except users_db.UserError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    session["must_change_password"] = False
    return jsonify({"ok": True})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    company_id = session.get("company_id")
    if company_id is not None:
        db.disconnect(company_id)
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/auth_status", methods=["GET"])
def api_auth_status():
    if not session.get("authenticated"):
        return jsonify({"authenticated": False})
    return jsonify({
        "authenticated": True,
        "email": session.get("email", ""),
        "role": session.get("role", "calisan"),
        "company": session.get("company_name", ""),
        "must_change_password": session.get("must_change_password", False),
    })


# --- Calisan yonetimi (sadece yonetici) -----------------------------------

@app.route("/api/employees", methods=["GET"])
@login_required
@yonetici_required
def api_list_employees():
    try:
        employees = users_db.list_employees(session["company_id"])
    except users_db.UserError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    return jsonify({"ok": True, "employees": employees})


@app.route("/api/add_employee", methods=["POST"])
@login_required
@yonetici_required
def api_add_employee():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    title = (data.get("title") or "").strip().lower()

    try:
        temp_password = users_db.add_employee(session["company_id"], email, title)
    except users_db.UserError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    company_name = session.get("company_name") or "AskQL"
    try:
        mailer.send_employee_invite_email(email, company_name, title, temp_password)
    except mailer.MailError as e:
        # Kullanici DB'de olusturuldu ama mail gitmedi -- yoneticiye gecici
        # sifreyi acikca goster ki calisana kendisi iletebilsin.
        return jsonify({
            "ok": True,
            "warning": f"Calisan eklendi ama davet e-postasi gonderilemedi: {e}. "
                       f"Gecici sifre: {temp_password}",
        })

    return jsonify({"ok": True})


# --- SQL Server baglantisi (sirket bazli, sadece yonetici kurar/gunceller) --

@app.route("/api/connect", methods=["POST"])
@login_required
@yonetici_required
def api_connect():
    """Sadece yonetici SQL baglantisi kurabilir/guncelleyebilir; bilgi sirket
    kaydina yazilir, boylece sirketteki tum calisanlar ayni baglantiyi
    otomatik kullanir (bkz. /api/auto_connect)."""
    data = request.get_json(force=True)
    server = (data.get("server") or "").strip()
    database = (data.get("database") or "").strip()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not all([server, database, username, password]):
        return jsonify({"ok": False, "error": "Sunucu, veritabani, kullanici adi ve sifre gerekli."}), 400

    company_id = session["company_id"]

    try:
        info = db.connect(company_id, server, database, username, password)
    except db.DBError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    try:
        users_db.save_company_connection(company_id, server, database, username, password)
    except users_db.UserError as e:
        return jsonify({"ok": False, "error": f"Baglanti kuruldu ama kaydedilemedi: {e}"}), 500

    session.pop("history", None)
    info["role"] = session.get("role")
    info["company"] = session.get("company_name")
    return jsonify({"ok": True, "info": info})


@app.route("/api/auto_connect", methods=["POST"])
@login_required
def api_auto_connect():
    """Sayfa acildiginda (ya da yonetici disindaki roller icin tek yol olarak)
    sirketin kayitli SQL bilgileriyle otomatik baglanmayi dener -- kullanici
    tekrar sunucu/sifre girmez."""
    company_id = session["company_id"]

    if db.is_connected(company_id):
        info = db.get_connection_info(company_id)
        info["role"] = session.get("role")
        info["company"] = session.get("company_name")
        return jsonify({"ok": True, "info": info})

    try:
        company = users_db.get_company(company_id)
    except users_db.UserError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    if not company.get("sql_server"):
        return jsonify({
            "ok": False,
            "error": "no_connection",
            "needs_setup": session.get("role") == "yonetici",
        }), 400

    try:
        info = db.connect(
            company_id,
            company["sql_server"], company["sql_database"],
            company["sql_username"], company["sql_password"],
        )
    except db.DBError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    session.pop("history", None)
    info["role"] = session.get("role")
    info["company"] = session.get("company_name")
    return jsonify({"ok": True, "info": info})


@app.route("/api/disconnect", methods=["POST"])
@login_required
@yonetici_required
def api_disconnect():
    db.disconnect(session["company_id"])
    session.pop("history", None)
    return jsonify({"ok": True})


@app.route("/api/status", methods=["GET"])
@login_required
def api_status():
    company_id = session["company_id"]
    if not db.is_connected(company_id):
        return jsonify({"connected": False})
    info = db.get_connection_info(company_id)
    info["role"] = session.get("role")
    info["company"] = session.get("company_name")
    return jsonify({"connected": True, "info": info})


@app.route("/api/reset_history", methods=["POST"])
@login_required
def api_reset_history():
    session.pop("history", None)
    return jsonify({"ok": True})


@app.route("/api/ask", methods=["POST"])
@login_required
def api_ask():
    """Kullanicinin dogal dil sorusunu/komutunu SQL'e cevirir.
    SELECT ise direkt calistirip sonucu + yorumu + grafigi dondurur.
    dml/ddl ise calistirmadan SQL'i onaya sunar."""
    company_id = session["company_id"]
    if not db.is_connected(company_id):
        return jsonify({"ok": False, "error": "Once bir veritabanina baglanmalisin."}), 400

    data = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    role = session.get("role", "calisan")

    if not question:
        return jsonify({"ok": False, "error": "Bir soru/komut yazmalisin."}), 400

    schema_text = db.get_schema_text(company_id)
    history_entries = session.get("history", [])
    history_messages = llm.build_history_messages(history_entries)

    try:
        result = llm.generate_sql_with_retry(
            question, schema_text, role, company_id, history=history_messages, max_attempts=3
        )
    except Exception as e:
        return jsonify({"ok": False, "error": f"SQL uretilemedi: {e}"}), 500

    sql = result.get("sql", "")

    if result.get("error") == "izin_yok":
        return jsonify({
            "ok": False,
            "error": "Bu islem senin unvanin icin izinli degil.",
        }), 403

    if result.get("error") == "rol_yetkisiz":
        if role == "calisan":
            msg = "Çalışan unvanında sadece SELECT sorgusu çalıştırılabilir."
        else:  # mudur
            msg = "Müdür unvanında tablo yapısını değiştiren (CREATE/ALTER/DROP/TRUNCATE) işlemler yapılamaz, bu sadece yönetici unvanına açık."
        return jsonify({"ok": False, "error": msg}), 403

    if result.get("error") == "eksik_bilgi":
        eksik = result.get("eksik_alanlar", [])
        eksik_metni = ", ".join(eksik) if eksik else "gerekli bazi bilgiler"
        return jsonify({
            "ok": False,
            "error": "eksik_bilgi",
            "eksik_alanlar": eksik,
            "message": f"Bu islemi yapabilmem icin su bilgiye ihtiyacim var: {eksik_metni}. "
                       f"{result.get('aciklama', '')}".strip(),
        }), 400

    if not result.get("ok"):
        return jsonify({"ok": False, "error": result.get("error", "Sorgu calistirilamadi."), "sql": sql}), 400

    if "columns" not in result:
        return jsonify({
            "ok": True,
            "type": "write",
            "sql": sql,
            "aciklama": result.get("aciklama", ""),
            "uyari": result.get("uyari", ""),
            "needs_confirmation": True,
        })

    columns = result["columns"]
    rows = result["rows"]

    try:
        chart_choice = llm.suggest_chart(question, sql, columns, rows)
    except Exception:
        chart_choice = {"chart_type": "none", "x_column": "", "y_column": "", "title": ""}

    try:
        interpretation = llm.interpret_results(question, sql, columns, rows)
    except Exception as e:
        interpretation = {"yorum": f"Yorum uretilemedi: {e}"}

    chart_data_url = chart.build_chart(
        chart_choice.get("chart_type", "none"),
        columns,
        rows,
        chart_choice.get("x_column", ""),
        chart_choice.get("y_column", ""),
        chart_choice.get("title", ""),
    )

    yorum_text = interpretation.get("yorum", "")
    history_entries.append({"question": question, "sql": sql, "summary": yorum_text[:300]})
    session["history"] = history_entries[-MAX_HISTORY:]

    return jsonify({
        "ok": True,
        "type": "select",
        "sql": sql,
        "columns": columns,
        "rows": rows[:100],
        "row_count": len(rows),
        "truncated": result.get("truncated", False),
        "yorum": yorum_text,
        "chart": chart_data_url,
    })


@app.route("/api/execute", methods=["POST"])
@login_required
def api_execute():
    """Kullanici DML/DDL sorgusunu onayladiktan sonra buraya dusen calistirma
    adimi. Rol/unvan kontrolu burada, bizim kodumuzda yapilir -- LLM'in bu
    kontrolu atlamasi mumkun degil."""
    company_id = session["company_id"]
    if not db.is_connected(company_id):
        return jsonify({"ok": False, "error": "Once bir veritabanina baglanmalisin."}), 400

    data = request.get_json(force=True)
    sql = (data.get("sql") or "").strip()
    role = session.get("role", "calisan")
    question = (data.get("question") or "Kullanicinin onayladigi yazma islemi").strip()

    actual_type = db.classify_query(sql)  # 'select' | 'dml' | 'ddl'

    if actual_type == "select":
        return jsonify({"ok": False, "error": "Bu SQL bir yazma sorgusu degil."}), 400
    if actual_type == "ddl" and role != "yonetici":
        return jsonify({"ok": False, "error": "Tablo yapisini degistiren (CREATE/ALTER/DROP/TRUNCATE) islemler sadece yonetici unvanina aciktir."}), 403
    if actual_type == "dml" and role not in ("yonetici", "mudur"):
        return jsonify({"ok": False, "error": "Yazma islemi icin en az mudur unvani gerekir."}), 403

    schema_text = db.get_schema_text(company_id)
    result = llm.execute_write_with_retry(question, schema_text, sql, company_id, max_attempts=3)

    if not result["ok"]:
        return jsonify({"ok": False, "error": result["error"], "sql": result["sql"]}), 400

    return jsonify({"ok": True, "affected_rows": result["affected_rows"], "sql": result["sql"]})


@app.route("/api/export", methods=["POST"])
@login_required
def api_export():
    """Sonuc tablosunu CSV veya PDF olarak disa aktarir. Uc unvan da (yonetici/
    mudur/calisan) zaten sadece kendi gorebildigi SELECT sonucunu export
    edebiliyor, bu yuzden burada ayrica bir unvan kontrolu gerekmiyor."""
    data = request.get_json(force=True)
    columns = data.get("columns") or []
    rows = data.get("rows") or []
    fmt = (data.get("format") or "csv").strip().lower()
    title = (data.get("title") or "rapor").strip() or "rapor"

    if not columns:
        return jsonify({"ok": False, "error": "Disa aktarilacak veri yok."}), 400

    safe_title = re.sub(r"[^a-zA-Z0-9_\-ığüşöçİĞÜŞÖÇ]+", "_", title)[:60] or "rapor"

    if fmt == "csv":
        content = report.build_csv(columns, rows)
        mem = io.BytesIO(content)
        return send_file(mem, mimetype="text/csv", as_attachment=True,
                          download_name=f"{safe_title}.csv")

    if fmt == "pdf":
        content = report.build_pdf(title, columns, rows)
        mem = io.BytesIO(content)
        return send_file(mem, mimetype="application/pdf", as_attachment=True,
                          download_name=f"{safe_title}.pdf")

    return jsonify({"ok": False, "error": "Desteklenmeyen format (csv veya pdf olmali)."}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
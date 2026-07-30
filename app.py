import os

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, render_template, request, session

import chart
import db
import llm

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-key")

MAX_HISTORY = 5


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/connect", methods=["POST"])
def api_connect():
    data = request.get_json(force=True)
    server = (data.get("server") or "").strip()
    database = (data.get("database") or "").strip()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not all([server, database, username, password]):
        return jsonify({"ok": False, "error": "Sunucu, veritabani, kullanici adi ve sifre gerekli."}), 400

    try:
        info = db.connect(server, database, username, password)
    except db.DBError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    # Rol artik beyana degil, veritabaninin bu girise verdigi gercek izne
    # gore belirlenir; sunucu tarafinda session'da tutulur, istemci degistiremez.
    session["role"] = info["role"]
    # Yeni baglantida onceki konusma gecmisi artik alakasiz -> temizle.
    session.pop("history", None)

    return jsonify({"ok": True, "info": info})


@app.route("/api/disconnect", methods=["POST"])
def api_disconnect():
    db.disconnect()
    session.pop("history", None)
    return jsonify({"ok": True})


@app.route("/api/status", methods=["GET"])
def api_status():
    if not db.is_connected():
        return jsonify({"connected": False})
    return jsonify({"connected": True, "info": db.get_connection_info()})


@app.route("/api/reset_history", methods=["POST"])
def api_reset_history():
    """Kullanici konusma gecmisini elle temizlemek isterse (ör. 'yeni sohbet' butonu)."""
    session.pop("history", None)
    return jsonify({"ok": True})


@app.route("/api/ask", methods=["POST"])
def api_ask():
    """Kullanicinin dogal dil sorusunu/komutunu SQL'e cevirir.
    SELECT ise direkt calistirip sonucu + yorumu + grafigi dondurur.
    write (DELETE/UPDATE/vb.) ise calistirmadan SQL'i onaya sunar.

    Pipeline:
      1) llm.generate_sql_with_retry -> Turkce soru (+ konusma gecmisi) -> SQL,
         hatali SQL'i sinirli sayida kendi kendine dener/duzeltir. Calistirma ve rol
         bazli guvenlik kontrolu HER ZAMAN bu fonksiyonun icinde, bizim kodumuzda yapilir.
      2) llm.suggest_chart     -> sonuc -> SADECE grafik turu/eksen karari
      3) llm.interpret_results -> sonuc -> SADECE Turkce yorum metni
    """
    if not db.is_connected():
        return jsonify({"ok": False, "error": "Once bir veritabanina baglanmalisin."}), 400

    data = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    # Rol istekten degil, baglanti aninda belirlenip session'a yazilan
    # degerden okunur -- istemci rolunu degistiremez.
    role = session.get("role", "analist")

    if not question:
        return jsonify({"ok": False, "error": "Bir soru/komut yazmalisin."}), 400

    schema_text = db.get_schema_text()
    history_entries = session.get("history", [])
    history_messages = llm.build_history_messages(history_entries)

    # --- 1) Adim: SQL uretimi + sinirli kendi-kendini-duzeltme ---
    try:
        result = llm.generate_sql_with_retry(
            question, schema_text, role, history=history_messages, max_attempts=3
        )
    except Exception as e:
        return jsonify({"ok": False, "error": f"SQL uretilemedi: {e}"}), 500

    sql = result.get("sql", "")

    if result.get("error") == "izin_yok":
        return jsonify({
            "ok": False,
            "error": "Bu islem analist rolu icin izinli degil (sadece SELECT calistirabilirsin).",
        }), 403

    if result.get("error") == "rol_yetkisiz":
        return jsonify({
            "ok": False,
            "error": "Analist rolunde sadece SELECT sorgusu calistirilabilir.",
        }), 403

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
        # write islemi: calistirmadan once onaya sun
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

    # --- 2) Adim: Grafik karari (yorumdan bagimsiz) ---
    try:
        chart_choice = llm.suggest_chart(question, sql, columns, rows)
    except Exception:
        chart_choice = {"chart_type": "none", "x_column": "", "y_column": "", "title": ""}

    # --- 3) Adim: Yorum metni (grafik kararindan bagimsiz) ---
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

    # Konusma gecmisini guncelle (sonraki sorularda baglam icin kullanilir).
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
        "yorum": yorum_text,
        "chart": chart_data_url,
    })


@app.route("/api/execute", methods=["POST"])
def api_execute():
    """Kullanici DELETE/UPDATE sorgusunu onayladiktan sonra buraya dusen calistirma adimi.
    Rol kontrolu burada, bizim kodumuzda yapilir -- LLM'in bu kontrolu atlamasi mumkun degil.
    DB hatasi olursa (ör. NOT NULL ihlali, tip uyusmazligi) sinirli sayida kendi kendini
    duzeltip tekrar dener (ayni SELECT akisindaki gibi)."""
    if not db.is_connected():
        return jsonify({"ok": False, "error": "Once bir veritabanina baglanmalisin."}), 400

    data = request.get_json(force=True)
    sql = (data.get("sql") or "").strip()
    role = session.get("role", "analist")
    # Onay ekranindan gelen orijinal soru; self-healing'e baglam saglar (opsiyonel).
    question = (data.get("question") or "Kullanicinin onayladigi yazma islemi").strip()

    if role != "yonetici":
        return jsonify({"ok": False, "error": "Sadece yonetici rolu yazma islemi onaylayabilir."}), 403

    if db.classify_query(sql) != "write":
        return jsonify({"ok": False, "error": "Bu SQL bir yazma sorgusu degil."}), 400

    schema_text = db.get_schema_text()
    result = llm.execute_write_with_retry(question, schema_text, sql, max_attempts=3)

    if not result["ok"]:
        return jsonify({"ok": False, "error": result["error"], "sql": result["sql"]}), 400

    return jsonify({"ok": True, "affected_rows": result["affected_rows"], "sql": result["sql"]})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

import os

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, render_template, request

import chart
import db
import llm

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-key")


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

    return jsonify({"ok": True, "info": info})


@app.route("/api/disconnect", methods=["POST"])
def api_disconnect():
    db.disconnect()
    return jsonify({"ok": True})


@app.route("/api/status", methods=["GET"])
def api_status():
    if not db.is_connected():
        return jsonify({"connected": False})
    return jsonify({"connected": True, "info": db.get_connection_info()})


@app.route("/api/ask", methods=["POST"])
def api_ask():
    """Kullanicinin dogal dil sorusunu/komutunu SQL'e cevirir.
    SELECT ise direkt calistirip sonucu + yorumu + grafigi dondurur.
    write (DELETE/UPDATE/vb.) ise calistirmadan SQL'i onaya sunar.
    """
    if not db.is_connected():
        return jsonify({"ok": False, "error": "Once bir veritabanina baglanmalisin."}), 400

    data = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    role = data.get("role") or "analist"

    if not question:
        return jsonify({"ok": False, "error": "Bir soru/komut yazmalisin."}), 400
    if role not in ("analist", "yonetici"):
        return jsonify({"ok": False, "error": "Gecersiz rol."}), 400

    schema_text = db.get_schema_text()

    try:
        sql_result = llm.generate_sql(question, schema_text, role)
    except Exception as e:
        return jsonify({"ok": False, "error": f"SQL uretilemedi: {e}"}), 500

    query_type = sql_result.get("query_type")
    sql = sql_result.get("sql", "")

    if query_type == "izin_yok":
        return jsonify({
            "ok": False,
            "error": "Bu islem analist rolu icin izinli degil (sadece SELECT calistirabilirsin).",
        }), 403

    # Guvenlik: LLM'in soyledigi tip ile SQL'in gercek tipi eslesmiyorsa gercek tipe guven
    actual_type = db.classify_query(sql)

    if role == "analist" and actual_type != "select":
        return jsonify({
            "ok": False,
            "error": "Analist rolunde sadece SELECT sorgusu calistirilabilir.",
        }), 403

    if actual_type == "select":
        try:
            columns, rows = db.run_select(sql)
        except db.DBError as e:
            # tek seferlik otomatik duzeltme denemesi
            try:
                fixed = llm.fix_sql(question, schema_text, role, sql, str(e))
                sql = fixed.get("sql", sql)
                if db.classify_query(sql) != "select":
                    raise db.DBError(str(e))
                columns, rows = db.run_select(sql)
            except db.DBError as e2:
                return jsonify({"ok": False, "error": str(e2), "sql": sql}), 400

        try:
            interpretation = llm.interpret_results(question, sql, columns, rows)
        except Exception as e:
            interpretation = {"yorum": f"Yorum uretilemedi: {e}", "chart_type": "none"}

        chart_data_url = chart.build_chart(
            interpretation.get("chart_type", "none"),
            columns,
            rows,
            interpretation.get("x_column", ""),
            interpretation.get("y_column", ""),
            interpretation.get("title", ""),
        )

        return jsonify({
            "ok": True,
            "type": "select",
            "sql": sql,
            "columns": columns,
            "rows": rows[:100],
            "row_count": len(rows),
            "yorum": interpretation.get("yorum", ""),
            "chart": chart_data_url,
        })

    else:
        # write islemi: calistirmadan once onaya sun
        return jsonify({
            "ok": True,
            "type": "write",
            "sql": sql,
            "aciklama": sql_result.get("aciklama", ""),
            "uyari": sql_result.get("uyari", ""),
            "needs_confirmation": True,
        })


@app.route("/api/execute", methods=["POST"])
def api_execute():
    """Kullanici DELETE/UPDATE sorgusunu onayladiktan sonra buraya dusen calistirma adimi."""
    if not db.is_connected():
        return jsonify({"ok": False, "error": "Once bir veritabanina baglanmalisin."}), 400

    data = request.get_json(force=True)
    sql = (data.get("sql") or "").strip()
    role = data.get("role") or "analist"

    if role != "yonetici":
        return jsonify({"ok": False, "error": "Sadece yonetici rolu yazma islemi onaylayabilir."}), 403

    if db.classify_query(sql) != "write":
        return jsonify({"ok": False, "error": "Bu SQL bir yazma sorgusu degil."}), 400

    try:
        affected = db.run_write(sql)
    except db.DBError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    return jsonify({"ok": True, "affected_rows": affected})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

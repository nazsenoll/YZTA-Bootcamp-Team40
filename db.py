"""
SQL Server baglanti ve sorgu calistirma islemleri.
Baglanti bilgisi tek kullanicilik demo icin process-icinde global olarak tutulur.
"""

import os
import re
import pyodbc

# Aktif baglanti bilgisi burada tutulur (tek kullanicili demo icin yeterli)
_state = {
    "conn": None,
    "server": None,
    "database": None,
    "schema": None,
    "role": None,
}

ODBC_DRIVER = os.environ.get("ODBC_DRIVER", "ODBC Driver 17 for SQL Server")


class DBError(Exception):
    pass


def connect(server: str, database: str, username: str, password: str) -> dict:
    """SQL Server'a kullanici adi/sifre ile baglanir. Onceki baglanti varsa kapatir."""
    disconnect()

    conn_str = (
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )

    try:
        conn = pyodbc.connect(conn_str, timeout=10)
    except pyodbc.Error as e:
        raise DBError(f"Baglanti kurulamadi: {e}")

    _state["conn"] = conn
    _state["server"] = server
    _state["database"] = database
    _state["schema"] = _read_schema(conn)
    _state["role"] = _determine_role(conn)

    return {
        "server": server,
        "database": database,
        "table_count": len(_state["schema"]),
        "role": _state["role"],
    }


def disconnect():
    if _state["conn"] is not None:
        try:
            _state["conn"].close()
        except Exception:
            pass
    _state["conn"] = None
    _state["server"] = None
    _state["database"] = None
    _state["schema"] = None
    _state["role"] = None


def is_connected() -> bool:
    return _state["conn"] is not None


def get_connection_info() -> dict:
    return {"server": _state["server"], "database": _state["database"], "role": _state["role"]}


def _determine_role(conn) -> str:
    """Baglanan SQL girisinin GERCEK veritabani izinlerine gore rolu belirler.
    Rol artik arayuzden secilen bir sey degil; hangi sifreyle baglanildiysa
    o girisin db_owner/db_datawriter uyeligine gore otomatik atanir."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT IS_MEMBER('db_owner'), IS_MEMBER('db_datawriter')")
        is_owner, is_writer = cursor.fetchone()
        return "yonetici" if (is_owner == 1 or is_writer == 1) else "analist"
    finally:
        cursor.close()


def get_schema() -> dict:
    if _state["schema"] is None:
        raise DBError("Once bir veritabanina baglanmalisin.")
    return _state["schema"]


def get_schema_text() -> str:
    """LLM promptuna gomulecek okunabilir sema metni.
    ZORUNLU etiketi: kolon NOT NULL ve varsayilan degeri yoksa -- bu durumda INSERT
    sirasinda deger MUTLAKA verilmelidir, aksi halde sorgu veritabani hatasiyla basarisiz olur.
    """
    schema = get_schema()
    lines = []
    for table, columns in schema.items():
        parts = []
        for c in columns:
            tag = ""
            if not c["nullable"] and not c["has_default"]:
                tag = " ZORUNLU"
            elif c["has_default"]:
                tag = " varsayilani_var"
            parts.append(f"{c['name']} ({c['type']}{tag})")
        col_desc = ", ".join(parts)
        lines.append(f"- {table}: {col_desc}")
    return "\n".join(lines)


def _read_schema(conn) -> dict:
    """Bagli veritabanindaki tablo, kolon, nullable ve default bilgilerini okur."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """
    )
    schema = {}
    for table_name, column_name, data_type, is_nullable, column_default in cursor.fetchall():
        schema.setdefault(table_name, []).append({
            "name": column_name,
            "type": data_type,
            "nullable": (is_nullable == "YES"),
            "has_default": column_default is not None,
        })
    cursor.close()
    return schema


# --- Sorgu turu tespiti ------------------------------------------------

_WRITE_KEYWORDS = re.compile(
    r"^\s*(DELETE|UPDATE|INSERT|DROP|TRUNCATE|ALTER|CREATE|EXEC|MERGE)\b",
    re.IGNORECASE,
)


def classify_query(sql: str) -> str:
    """SQL'in 'select' mi yoksa 'write' (DELETE/UPDATE/vb.) mi oldugunu dondurur."""
    stripped = sql.strip()
    if _WRITE_KEYWORDS.match(stripped):
        return "write"
    return "select"


def run_select(sql: str, max_rows: int = 500):
    """Sadece SELECT sorgulari icin. Kolon isimlerini ve satirlari dondurur."""
    if classify_query(sql) != "select":
        raise DBError("Bu fonksiyon sadece SELECT sorgulari icin kullanilabilir.")
    if _state["conn"] is None:
        raise DBError("Once bir veritabanina baglanmalisin.")

    cursor = _state["conn"].cursor()
    try:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchmany(max_rows)
        rows = [list(row) for row in rows]
    except pyodbc.Error as e:
        raise DBError(f"Sorgu calistirilamadi: {e}")
    finally:
        cursor.close()

    return columns, rows


def run_write(sql: str) -> int:
    """DELETE/UPDATE vb. sorgular icin. Sadece kullanici onayindan sonra cagrilmali."""
    if classify_query(sql) != "write":
        raise DBError("Bu fonksiyon sadece yazma sorgulari icin kullanilabilir.")
    if _state["conn"] is None:
        raise DBError("Once bir veritabanina baglanmalisin.")

    cursor = _state["conn"].cursor()
    try:
        cursor.execute(sql)
        affected = cursor.rowcount
        _state["conn"].commit()
    except pyodbc.Error as e:
        _state["conn"].rollback()
        raise DBError(f"Sorgu calistirilamadi: {e}")
    finally:
        cursor.close()

    return affected

"""
SQL Server baglanti ve sorgu calistirma islemleri.

Uygulama cok kiracili (multi-tenant): birden fazla sirket ayni Flask
sureci uzerinde calisabiliyor. Bu yuzden baglanti tek bir global degil,
company_id -> baglanti bilgisi seklinde bir sozlukte tutulur.
"""

import os
import re
import pyodbc

# company_id -> {"conn":..., "server":..., "database":..., "schema":...}
_connections: dict = {}

ODBC_DRIVER = os.environ.get("ODBC_DRIVER", "ODBC Driver 17 for SQL Server")


class DBError(Exception):
    pass


def connect(company_id, server: str, database: str, username: str, password: str) -> dict:
    disconnect(company_id)

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

    try:
        schema = _read_schema(conn)
    except pyodbc.Error as e:
        try:
            conn.close()
        except Exception:
            pass
        raise DBError(f"Semaya erisilemedi: {e}")

    _connections[company_id] = {
        "conn": conn,
        "server": server,
        "database": database,
        "schema": schema,
    }

    return {
        "server": server,
        "database": database,
        "table_count": len(schema),
    }


def disconnect(company_id):
    entry = _connections.pop(company_id, None)
    if entry and entry.get("conn") is not None:
        try:
            entry["conn"].close()
        except Exception:
            pass


def is_connected(company_id) -> bool:
    return company_id in _connections and _connections[company_id].get("conn") is not None


def get_connection_info(company_id) -> dict:
    entry = _connections.get(company_id)
    if not entry:
        raise DBError("Once bir veritabanina baglanmalisin.")
    return {"server": entry["server"], "database": entry["database"]}


def get_schema(company_id) -> dict:
    entry = _connections.get(company_id)
    if not entry:
        raise DBError("Once bir veritabanina baglanmalisin.")
    return entry["schema"]


def get_schema_text(company_id) -> str:
    schema = get_schema(company_id)
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


_DML_KEYWORDS = re.compile(r"^\s*(INSERT|UPDATE|DELETE|MERGE)\b", re.IGNORECASE)
_DDL_KEYWORDS = re.compile(r"^\s*(DROP|TRUNCATE|ALTER|CREATE|EXEC|EXECUTE)\b", re.IGNORECASE)

_DML_KEYWORD_ANYWHERE = re.compile(r"\b(INSERT|UPDATE|DELETE|MERGE)\b", re.IGNORECASE)
_DDL_KEYWORD_ANYWHERE = re.compile(r"\b(DROP|TRUNCATE|ALTER|CREATE|EXEC|EXECUTE)\b", re.IGNORECASE)

_LINE_COMMENT = re.compile(r"--[^\n]*")
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_MD_FENCE = re.compile(r"```(?:sql)?", re.IGNORECASE)


def _normalize_sql(sql: str) -> str:
    cleaned = _MD_FENCE.sub("", sql)
    cleaned = _BLOCK_COMMENT.sub(" ", cleaned)
    cleaned = _LINE_COMMENT.sub(" ", cleaned)
    return cleaned.strip()


def classify_query(sql: str) -> str:
    cleaned = _normalize_sql(sql)

    statements = [s for s in cleaned.split(";") if s.strip()]
    if len(statements) > 1:
        return "ddl"

    if _DDL_KEYWORDS.match(cleaned):
        return "ddl"
    if _DML_KEYWORDS.match(cleaned):
        return "dml"

    if not cleaned.upper().startswith("SELECT"):
        if _DDL_KEYWORD_ANYWHERE.search(cleaned):
            return "ddl"
        if _DML_KEYWORD_ANYWHERE.search(cleaned):
            return "dml"
        if not cleaned.upper().startswith("WITH"):
            return "ddl"

    return "select"


def run_select(company_id, sql: str, max_rows: int = 500):
    if classify_query(sql) != "select":
        raise DBError("Bu fonksiyon sadece SELECT sorgulari icin kullanilabilir.")
    entry = _connections.get(company_id)
    if not entry:
        raise DBError("Once bir veritabanina baglanmalisin.")

    cursor = entry["conn"].cursor()
    try:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchmany(max_rows + 1)
        rows = [list(row) for row in rows]
    except pyodbc.Error as e:
        raise DBError(f"Sorgu calistirilamadi: {e}")
    finally:
        cursor.close()

    truncated = len(rows) > max_rows
    if truncated:
        rows = rows[:max_rows]

    return columns, rows, truncated


def run_write(company_id, sql: str) -> int:
    if classify_query(sql) not in ("dml", "ddl"):
        raise DBError("Bu fonksiyon sadece yazma sorgulari icin kullanilabilir.")
    entry = _connections.get(company_id)
    if not entry:
        raise DBError("Once bir veritabanina baglanmalisin.")

    cursor = entry["conn"].cursor()
    try:
        cursor.execute(sql)
        affected = cursor.rowcount
        entry["conn"].commit()
    except pyodbc.Error as e:
        entry["conn"].rollback()
        raise DBError(f"Sorgu calistirilamadi: {e}")
    finally:
        cursor.close()

    return affected
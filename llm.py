"""
OpenAI cagrilarini yoneten modul. Iki gorev var:
1) generate_sql: Turkce soru + sema -> SQL sorgusu
2) interpret_results: sorgu sonucu -> Turkce yorum + grafik onerisi
Not: Bu bir agent degil, sabit iki adimli bir pipeline'dir. LLM hicbir zaman
kendi kendine ne zaman calisacagina karar vermez, sirali olarak cagrilir.
"""

import json
import os
from openai import OpenAI

_client = None
MODEL = "gpt-4o-mini"


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY bulunamadi. .env dosyani kontrol et.")
        _client = OpenAI(api_key=api_key)
    return _client


SQL_SYSTEM_PROMPT = """Sen bir SQL Server uzmanisin. Kullanicinin Turkce sorusunu/komutunu
verilen veritabani semasina gore T-SQL sorgusuna cevirirsin.

Kurallar:
- Sadece verilen tablo ve kolon isimlerini kullan, uydurma.
- Kullanici rolu "analist" ise SADECE SELECT sorgusu uret. Baska bir sey istese bile
  SELECT disinda bir sorgu uretme, bunun yerine "izin_yok" olarak isaretle.
- Kullanici rolu "yonetici" ise SELECT, DELETE, UPDATE, INSERT uretebilirsin.
- WHERE kosulu olmadan DELETE/UPDATE uretme (tum tabloyu etkileyecek sorgulardan kacin),
  eger kullanici gercekten tum satirlari hedefliyorsa bunu "uyari" alaninda belirt.
- Cok satir donebilecek SELECT sorgularina TOP 200 ekle.
- Yalnizca gecerli T-SQL uret, aciklama veya markdown ekleme.

Sadece asagidaki JSON formatinda cevap ver:
{
  "sql": "...",
  "query_type": "select" | "write" | "izin_yok",
  "aciklama": "sorgunun ne yaptigina dair 1 cumlelik Turkce aciklama",
  "uyari": "riskli bir durum varsa kisa uyari, yoksa bos string"
}
"""

INTERPRET_SYSTEM_PROMPT = """Sen bir veri analistisin. Sana bir Turkce soru, calistirilan SQL
sorgusu ve sonuc satirlari verilecek. Gorevin:
1) Sonucu sade, is diline uygun Turkce ile yorumlamak (2-4 cumle, somut sayilarla).
2) Sonucu gorsellestirmek icin en uygun grafik turunu onermek.

Grafik kurallari:
- Sonuc tek bir satir/sayi ise chart_type "none" olsun.
- Kategori karsilastirmasi ise "bar", zaman serisi ise "line", oran/pay ise "pie" sec.
- x_column ve y_column, sonuc kolon isimlerinden birebir olmali.
- Kolon sayisi veya veri grafige uygun degilse chart_type "none" yap.

Sadece asagidaki JSON formatinda cevap ver:
{
  "yorum": "...",
  "chart_type": "bar" | "line" | "pie" | "none",
  "x_column": "..." ,
  "y_column": "...",
  "title": "grafik basligi"
}
"""


def generate_sql(question: str, schema_text: str, role: str) -> dict:
    client = _get_client()
    user_prompt = f"""Veritabani semasi:
{schema_text}

Kullanici rolu: {role}
Kullanici sorusu/komutu: {question}
"""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SQL_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return json.loads(response.choices[0].message.content)


def fix_sql(question: str, schema_text: str, role: str, failed_sql: str, error_message: str) -> dict:
    """Hatali SQL icin tek seferlik duzeltme denemesi (loop degil, sabit tek deneme)."""
    client = _get_client()
    user_prompt = f"""Veritabani semasi:
{schema_text}

Kullanici rolu: {role}
Kullanici sorusu/komutu: {question}

Az once uretilen sorgu calisirken hata verdi:
SQL: {failed_sql}
Hata: {error_message}

Bu hatayi dikkate alarak sorguyu duzelt.
"""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SQL_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return json.loads(response.choices[0].message.content)


def interpret_results(question: str, sql: str, columns: list, rows: list) -> dict:
    client = _get_client()
    # Buyuk sonuc setlerinde LLM'e sadece bir ornek gonder
    preview_rows = rows[:30]
    user_prompt = f"""Soru: {question}
SQL: {sql}
Kolonlar: {columns}
Satirlar (ilk {len(preview_rows)} tanesi, toplam {len(rows)} satir): {preview_rows}
"""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": INTERPRET_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return json.loads(response.choices[0].message.content)

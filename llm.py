"""
LangChain tabanli OpenAI cagri katmani. UC AYRI, BIRBIRINDEN BAGIMSIZ LLM gorevi vardir,
her biri kendi Pydantic seması ve prompt'u ile ayri bir chain'dir:

1) generate_sql / fix_sql   : Turkce soru + sema (+ konusma gecmisi) -> SQL sorgusu
2) suggest_chart            : sorgu sonucu -> SADECE grafik turu + eksen secimi
3) interpret_results        : sorgu sonucu -> SADECE Turkce yorum metni

Ayrica generate_sql_with_retry: sinirli sayida (varsayilan 3) kendi kendini duzelten bir
dongu calistirir -- "agent" davranisina benzer ama ONEMLI FARK: SQL'i calistirma ve rol
bazli guvenlik kontrolu HER ZAMAN bizim Python kodumuzda yapilir. LLM hicbir zaman SQL'i
dogrudan calistiramaz ya da guvenlik kontrolunu atlayamaz; sadece metin/SQL onerisi uretir.

Konusma hafizasi: cagiran taraf (app.py) onceki soru-cevaplari `history` olarak
(LangChain mesaj listesi) gecebilir; boylece "peki ya gecen ay?" gibi baglama atifli
sorular cozulebilir.
"""

import os
from typing import Literal, Optional

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

import db

MODEL = "gpt-4o-mini"

_llm_cache: dict[float, ChatOpenAI] = {}


def _get_llm(temperature: float = 0) -> ChatOpenAI:
    if temperature not in _llm_cache:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY bulunamadi. .env dosyani kontrol et.")
        _llm_cache[temperature] = ChatOpenAI(model=MODEL, temperature=temperature, api_key=api_key)
    return _llm_cache[temperature]


def build_history_messages(history_entries: Optional[list]) -> list:
    """Flask session'da tutulan [{"question":..,"sql":..,"summary":..}, ...] (eskiden yeniye)
    listesini LangChain mesajlarina cevirir. Sadece SQL uretim adiminda baglam icin kullanilir."""
    if not history_entries:
        return []
    messages = []
    for entry in history_entries[-5:]:
        messages.append(HumanMessage(content=entry.get("question", "")))
        ai_content = f"Calistirilan SQL: {entry.get('sql', '')}\nSonuc ozeti: {entry.get('summary', '')}"
        messages.append(AIMessage(content=ai_content))
    return messages


# ==========================================================================
# 1) SQL URETIMI
# ==========================================================================

class SqlGenerationResult(BaseModel):
    sql: str = Field(default="", description="Uretilen T-SQL sorgusu (eksik_bilgi durumunda bos birakilabilir)")
    query_type: Literal["select", "write", "izin_yok", "eksik_bilgi"]
    aciklama: str = Field(description="Sorgunun ne yaptigina dair 1 cumlelik Turkce aciklama")
    uyari: str = Field(default="", description="Riskli bir durum varsa kisa uyari, yoksa bos string")
    eksik_alanlar: list[str] = Field(
        default_factory=list,
        description="query_type 'eksik_bilgi' ise, kullanicidan istenmesi gereken alan adlari",
    )


SQL_SYSTEM_PROMPT = """Sen bir SQL Server uzmanisin. Kullanicinin Turkce sorusunu/komutunu
verilen veritabani semasina gore T-SQL sorgusuna cevirirsin.

Kurallar:
- Sadece verilen tablo ve kolon isimlerini kullan, uydurma.
- Kullanici rolu "calisan" ise SADECE SELECT sorgusu uret. Baska bir sey istese bile
  SELECT disinda bir sorgu uretme, bunun yerine "izin_yok" olarak isaretle.
- Kullanici rolu "mudur" ise SELECT, INSERT, UPDATE, DELETE uretebilirsin. Ancak
  CREATE, ALTER, DROP, TRUNCATE gibi TABLO YAPISINI degistiren islemler uretme --
  bunlar sadece "yonetici" rolune aciktir; mudur boyle bir sey isterse "izin_yok"
  olarak isaretle.
- Kullanici rolu "yonetici" ise SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER,
  DROP, TRUNCATE uretebilirsin (tablo ekleme/kaldirma dahil, tüm işlemler serbest).
- WHERE kosulu olmadan DELETE/UPDATE uretme (tum tabloyu etkileyecek sorgulardan kacin),
  eger kullanici gercekten tum satirlari hedefliyorsa bunu "uyari" alaninda belirt.
- Cok satir donebilecek SELECT sorgularina TOP 200 ekle.
- Yalnizca gecerli T-SQL uret, aciklama veya markdown ekleme.
- Konusma gecmisinde onceki soru/SQL/sonuclar varsa, kullanicinin "peki ya gecen ay",
  "onu da X'e gore grupla" gibi ATIFLI (baglama bagli) sorularini gecmise bakarak coz.
  Gecmis yoksa ya da soru bagimsizsa, sadece mevcut soruya odaklan.

ZORUNLU (NOT NULL, varsayilani olmayan) kolonlar hakkinda COK ONEMLI kural:
- Semada bir kolon "ZORUNLU" olarak isaretlenmisse, o kolona INSERT sirasinda MUTLAKA
  gecerli bir deger verilmelidir. Boyle bir kolon icin degeri UYDURMA ve ASLA NULL yazma.
- Kullanicinin sorusunda o zorunlu kolon icin acik ya da makul sekilde cikarilabilir bir
  deger (ör. tarih icin GETDATE(), miktar icin 0) YOKSA, SQL uretme: query_type'i
  "eksik_bilgi" olarak isaretle, sql alanini bos birak, ve "eksik_alanlar" listesine o
  kolonlarin adlarini yaz (ör. ["Satis_Bolgesi"]). aciklama alaninda kullaniciya hangi
  bilgi(ler)i vermesi gerektigini kisaca sor.
- Sadece gercekten mantikli/varsayilan bir deger cikarilabiliyorsa (ör. tarih kolonlarina
  GETDATE(), otomatik artan/identity kolonlara deger verme) INSERT'i tamamla.
"""

_sql_prompt = ChatPromptTemplate.from_messages([
    ("system", SQL_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history", optional=True),
    ("human", "{user_input}"),
])


def _sql_chain():
    return _sql_prompt | _get_llm(temperature=0).with_structured_output(SqlGenerationResult)


def generate_sql(question: str, schema_text: str, role: str, history: Optional[list] = None) -> dict:
    user_input = f"""Veritabani semasi:
{schema_text}

Kullanici rolu: {role}
Kullanici sorusu/komutu: {question}
"""
    result = _sql_chain().invoke({"history": history or [], "user_input": user_input})
    return result.model_dump()


def fix_sql(question: str, schema_text: str, role: str, failed_sql: str, error_message: str) -> dict:
    """Hatali SQL icin duzeltme denemesi (generate_sql_with_retry icinde sinirli sayida cagrilir)."""
    user_input = f"""Veritabani semasi:
{schema_text}

Kullanici rolu: {role}
Kullanici sorusu/komutu: {question}

Az once uretilen sorgu calisirken hata verdi:
SQL: {failed_sql}
Hata: {error_message}

Bu hatayi dikkate alarak sorguyu duzelt.
"""
    result = _sql_chain().invoke({"history": [], "user_input": user_input})
    return result.model_dump()


def generate_sql_with_retry(question: str, schema_text: str, role: str, company_id,
                             history: Optional[list] = None, max_attempts: int = 3) -> dict:
    """Sinirli kendi-kendini-duzeltme donguesu. SQL calistirma ve rol bazli guvenlik
    kontrolu HER ZAMAN burada, bizim kodumuzda yapilir -- LLM bu kontrolleri hicbir
    zaman atlayamaz. company_id, hangi sirketin baglantisi uzerinden calistirilacagini
    belirler (bkz. db.py -- baglantilar artik sirket bazli tutuluyor).

    Donen dict alanlari:
      - her zaman: sql, query_type, aciklama, uyari, ok, error
      - basarili SELECT: columns, rows de eklenir
      - write (onay bekleyen): columns/rows yoktur, ok=True, error=None
      - izin_yok / rol_yetkisiz: ok=False, error bu degerlerden biri
    """
    sql_result = generate_sql(question, schema_text, role, history=history)
    query_type = sql_result.get("query_type")
    sql = sql_result.get("sql", "")

    if query_type == "izin_yok":
        return {**sql_result, "ok": False, "error": "izin_yok"}

    if query_type == "eksik_bilgi":
        return {**sql_result, "ok": False, "error": "eksik_bilgi"}

    actual_type = db.classify_query(sql)  # 'select' | 'dml' | 'ddl'

    if role == "calisan" and actual_type != "select":
        return {**sql_result, "ok": False, "error": "rol_yetkisiz"}
    if role == "mudur" and actual_type == "ddl":
        return {**sql_result, "ok": False, "error": "rol_yetkisiz"}
    # role == "yonetici": select/dml/ddl hepsine izinli

    if actual_type != "select":
        return {**sql_result, "sql": sql, "ok": True, "error": None}

    last_error = None
    for attempt in range(max_attempts):
        try:
            columns, rows, truncated = db.run_select(company_id, sql)
            return {**sql_result, "sql": sql, "ok": True, "error": None,
                     "columns": columns, "rows": rows, "truncated": truncated}
        except db.DBError as e:
            last_error = str(e)
            if attempt == max_attempts - 1:
                break
            fixed = fix_sql(question, schema_text, role, sql, last_error)
            sql = fixed.get("sql", sql)
            if db.classify_query(sql) != "select":
                break

    return {**sql_result, "sql": sql, "ok": False, "error": last_error}


def execute_write_with_retry(question: str, schema_text: str, sql: str, company_id,
                              max_attempts: int = 3) -> dict:
    """Onaylanmis bir yazma (dml/ddl) sorgusunu calistirir; DB hatasi alirsa
    sinirli sayida fix_sql ile duzeltip tekrar dener. Rol kontrolu BU
    FONKSIYONDAN ONCE, cagiran tarafta (app.py) yapilmis olmali.

    Donen dict: {"ok": bool, "sql": son_denenen_sql, "affected_rows": int|None, "error": str|None}
    """
    last_error = None
    current_sql = sql
    for attempt in range(max_attempts):
        try:
            affected = db.run_write(company_id, current_sql)
            return {"ok": True, "sql": current_sql, "affected_rows": affected, "error": None}
        except db.DBError as e:
            last_error = str(e)
            if attempt == max_attempts - 1:
                break
            fixed = fix_sql(question, schema_text, "yonetici", current_sql, last_error)
            candidate = fixed.get("sql", current_sql)
            if db.classify_query(candidate) not in ("dml", "ddl"):
                break
            current_sql = candidate

    return {"ok": False, "sql": current_sql, "affected_rows": None, "error": last_error}


# ==========================================================================
# 2) GRAFIK SECIMI -- SADECE grafik turu + eksenler, YORUM YAZMAZ
# ==========================================================================

class ChartSuggestion(BaseModel):
    chart_type: Literal["bar", "line", "pie", "area", "scatter", "histogram", "none"]
    x_column: str = ""
    y_column: str = ""
    title: str = ""


CHART_SYSTEM_PROMPT = """Sen bir veri gorsellestirme uzmanisin. Sana bir Turkce soru, calistirilan
SQL sorgusu ve sonuc satirlari verilecek. TEK GOREVIN sonucu gorsellestirmek icin en uygun
grafik turunu ve hangi kolonlarin hangi eksende kullanilacagini secmek. Yorum/aciklama YAZMA,
sadece grafik karari ver.

Secebilecegin grafik turleri:
- "bar"       : kategoriler arasi karsilastirma / siralama (ör. en cok satan urunler)
- "line"      : zaman serisi / sirali trend (ör. aylara gore ciro)
- "pie"       : bir butunun kategoriler arasindaki PAYI/ORANI, en fazla ~8 kategori icin uygun
- "area"      : zaman icinde kumulatif/hacimsel degisim
- "scatter"   : iki sayisal degisken arasindaki iliski (x_column ve y_column ikisi de sayisal olmali)
- "histogram" : tek bir sayisal kolonun dagilimi (sadece x_column doldur, y_column bos birak)
- "none"      : sonuc tek bir satir/sayi ise veya veri hicbir grafik turune uygun degilse

GRAFIK TURU SECIM ONCELIGI (sirayla uygula):
1) ONCE kullanicinin sorusunda ACIK bir grafik turu istegi var mi kontrol et. Asagidaki
   anahtar kelimeler gecerse o turu ZORUNLU olarak sec, baska hicbir kurala bakma:
   - "pasta", "dilim", "pie"                -> "pie"
   - "cizgi", "line", "trend", "zaman ici"  -> "line"
   - "sutun", "bar", "cubuk"                -> "bar"
   - "alan", "area"                          -> "area"
   - "sacilim", "scatter", "iliski"          -> "scatter"
   - "histogram", "dagilim grafigi"          -> "histogram"
2) Acik bir istek YOKSA ve sonuc kucuk sayida kategori iceriyorsa (<= 8 satir) VE soru bir
   siralama/karsilastirma vurgusu tasimiyorsa ("en cok", "en yuksek", "en dusuk", "sirala",
   "karsilastir" gibi ifadeler YOKSA) -> bu, bir butunun kategoriler arasindaki PAYINI
   gosterme istegidir, "pie" sec (bar degil).
3) Acik bir istek yoksa ve soru siralama/karsilastirma vurgusu tasiyorsa veya kategori sayisi
   8'den fazlaysa -> "bar" sec.
4) Zaman/tarih/ay/yil bazli sirali veri ise -> "line" (veya "area") sec.
5) Hicbiri uymuyorsa -> "none" sec.

Kurallar:
- x_column ve y_column, sonuc kolon isimlerinden BIREBIR olmali.
- histogram icin y_column'u bos string "" birak.
- Kolon sayisi veya veri turu (ör. metin kolonlarla scatter) uygun degilse "none" sec.
- Emin degilsen "bar" yerine "none" secmek her zaman daha güvenlidir.
"""

_chart_prompt = ChatPromptTemplate.from_messages([
    ("system", CHART_SYSTEM_PROMPT),
    ("human", "{user_input}"),
])


def suggest_chart(question: str, sql: str, columns: list, rows: list) -> dict:
    """SADECE grafik turu ve eksen secimini dondurur. Yorum icermez."""
    chain = _chart_prompt | _get_llm(temperature=0).with_structured_output(ChartSuggestion)
    preview_rows = rows[:30]
    user_input = f"""Soru: {question}
SQL: {sql}
Kolonlar: {columns}
Satirlar (ilk {len(preview_rows)} tanesi, toplam {len(rows)} satir): {preview_rows}
"""
    result = chain.invoke({"user_input": user_input})
    return result.model_dump()


# ==========================================================================
# 3) SONUC YORUMU -- SADECE Turkce metin yorumu, GRAFIK KARARI VERMEZ
# ==========================================================================

class Interpretation(BaseModel):
    yorum: str


INTERPRET_SYSTEM_PROMPT = """Sen bir veri analistisin. Sana bir Turkce soru, calistirilan SQL
sorgusu ve sonuc satirlari verilecek. TEK GOREVIN, kullanicinin SORDUGU SEYE cevap veren
kisa bir Turkce yorum yazmak (2-4 cumle, somut sayilarla). Grafik turu, eksen ya da
gorsellestirme ile ILGILENME, sadece metin yorum yaz.

COK ONEMLI - ASIRI YORUMLAMA YAPMA:
- Soruda gecmeyen bir cerceve/vurgu UYDURMA. Ozellikle:
  - Kullanici "en yuksek", "en cok", "en dusuk", "sirala", "karsilastir" gibi bir sey
    SORMADIYSA, cevabinda "en yuksek ... kategorisidir", "ilk sirada ... yer aliyor" gibi
    siralama/karsilastirma dili KULLANMA.
  - Kullanici sadece bir grafik/dagilim/pay gormek istediyse (ör. "pasta grafigini istiyorum",
    "dagilimini goster"), yorumun da notr bir sekilde veriyi ve oranlari ozetlesin; hangisinin
    "en iyi/en yuksek" oldugunu vurgulama.
  - Kullanici acikca siralama/karsilastirma SORDUYSA, o zaman en yuksek/en dusuk gibi
    ifadeleri rahatlikla kullanabilirsin.
- Kisacasi: yorumun her zaman soruya sadik kalsin, veriden kendiliginden ek bir sonuc/vurgu
  cikarma.
"""

_interpret_prompt = ChatPromptTemplate.from_messages([
    ("system", INTERPRET_SYSTEM_PROMPT),
    ("human", "{user_input}"),
])


def interpret_results(question: str, sql: str, columns: list, rows: list) -> dict:
    """SADECE Turkce yorum metnini dondurur. Grafik karari icermez."""
    chain = _interpret_prompt | _get_llm(temperature=0.3).with_structured_output(Interpretation)
    preview_rows = rows[:30]
    user_input = f"""Soru: {question}
SQL: {sql}
Kolonlar: {columns}
Satirlar (ilk {len(preview_rows)} tanesi, toplam {len(rows)} satir): {preview_rows}
"""
    result = chain.invoke({"user_input": user_input})
    return result.model_dump()
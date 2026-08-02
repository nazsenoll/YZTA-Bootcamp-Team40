"""
CSV/PDF rapor disa aktarma yardimcilari.

PDF uretimi icin ekstra bir bagimlilik eklememek adina, projede zaten
kullanilan matplotlib'in PdfPages ozelligiyle sonuc satirlari bir tablo
olarak sayfa(lar)a cizilir.
"""

import csv
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROWS_PER_PAGE = 25


def build_csv(columns: list, rows: list) -> bytes:
    """UTF-8 BOM'lu CSV uretir -- BOM olmadan Excel Turkce karakterleri
    (ör. ğ, ş, ç) bozuk gosterebiliyor."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(columns)
    for row in rows:
        writer.writerow(["" if c is None else c for c in row])
    return buf.getvalue().encode("utf-8-sig")


def build_pdf(title: str, columns: list, rows: list) -> bytes:
    """Sonuc satirlarini sayfa basina ROWS_PER_PAGE satir olacak sekilde
    coklu-sayfa bir PDF tablosuna cizer."""
    buf = io.BytesIO()
    chunks = [rows[i:i + ROWS_PER_PAGE] for i in range(0, len(rows), ROWS_PER_PAGE)] or [[]]

    with PdfPages(buf) as pdf:
        for page_idx, chunk in enumerate(chunks):
            fig, ax = plt.subplots(figsize=(11.7, 8.3))  # A4 yatay
            ax.axis("off")
            page_suffix = f" ({page_idx + 1}/{len(chunks)})" if len(chunks) > 1 else ""
            ax.set_title(f"{title}{page_suffix}", fontsize=14, fontweight="bold", pad=20)

            display_rows = [["" if c is None else str(c) for c in row] for row in chunk]
            if display_rows:
                table = ax.table(cellText=display_rows, colLabels=columns, loc="center", cellLoc="left")
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1, 1.4)
            else:
                ax.text(0.5, 0.5, "Sonuc bulunamadi.", ha="center", va="center", fontsize=11)

            pdf.savefig(fig)
            plt.close(fig)

    return buf.getvalue()
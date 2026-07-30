"""Sonuc verisinden matplotlib grafigi uretip base64 PNG olarak dondurur.

Bu modul, llm.suggest_chart'in verdigi karara (chart_type, x_column, y_column, title)
gore SADECE cizim yapar. Hangi grafik turunun secilecegine burada karar verilmez.
Desteklenen turler: bar, line, pie, area, scatter, histogram.
"""

import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_COLOR = "#2f6f6f"


def _to_floats(rows, idx):
    try:
        return [float(row[idx]) for row in rows]
    except (TypeError, ValueError):
        return None


def build_chart(chart_type: str, columns: list, rows: list, x_column: str, y_column: str, title: str):
    if chart_type == "none" or not rows:
        return None
    if x_column not in columns:
        return None
    # histogram sadece x_column kullanir, digerleri y_column da ister
    if chart_type != "histogram" and y_column not in columns:
        return None

    x_idx = columns.index(x_column)
    y_idx = columns.index(y_column) if y_column in columns else None
    labels = [str(row[x_idx]) for row in rows]

    fig, ax = plt.subplots(figsize=(7, 4.2))

    if chart_type == "histogram":
        values = _to_floats(rows, x_idx)
        if values is None:
            plt.close(fig)
            return None
        bins = max(5, min(20, len(values) // 2 or 1))
        ax.hist(values, bins=bins, color=_COLOR, edgecolor="#10161a")
        ax.set_xlabel(x_column)
        ax.set_ylabel("Frekans")

    elif chart_type == "bar":
        values = _to_floats(rows, y_idx)
        if values is None:
            plt.close(fig)
            return None
        ax.bar(labels, values, color=_COLOR)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        plt.xticks(rotation=30, ha="right")

    elif chart_type == "line":
        values = _to_floats(rows, y_idx)
        if values is None:
            plt.close(fig)
            return None
        ax.plot(labels, values, marker="o", color=_COLOR)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        plt.xticks(rotation=30, ha="right")

    elif chart_type == "area":
        values = _to_floats(rows, y_idx)
        if values is None:
            plt.close(fig)
            return None
        xs = range(len(labels))
        ax.fill_between(xs, values, color=_COLOR, alpha=0.35)
        ax.plot(xs, values, color=_COLOR)
        ax.set_xticks(list(xs))
        ax.set_xticklabels(labels, rotation=30, ha="right")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

    elif chart_type == "scatter":
        x_values = _to_floats(rows, x_idx)
        y_values = _to_floats(rows, y_idx)
        if x_values is None or y_values is None:
            plt.close(fig)
            return None
        ax.scatter(x_values, y_values, color=_COLOR)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

    elif chart_type == "pie":
        values = _to_floats(rows, y_idx)
        if values is None:
            plt.close(fig)
            return None
        ax.pie(values, labels=labels, autopct="%1.1f%%", colors=plt.cm.Set2.colors)

    else:
        plt.close(fig)
        return None

    ax.set_title(title)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140)
    plt.close(fig)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
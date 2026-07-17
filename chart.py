"""Sonuc verisinden matplotlib grafigi uretip base64 PNG olarak dondurur."""

import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def build_chart(chart_type: str, columns: list, rows: list, x_column: str, y_column: str, title: str):
    if chart_type == "none" or not rows:
        return None
    if x_column not in columns or y_column not in columns:
        return None

    x_idx = columns.index(x_column)
    y_idx = columns.index(y_column)

    labels = [str(row[x_idx]) for row in rows]
    try:
        values = [float(row[y_idx]) for row in rows]
    except (TypeError, ValueError):
        return None

    fig, ax = plt.subplots(figsize=(7, 4.2))

    if chart_type == "bar":
        ax.bar(labels, values, color="#2f6f6f")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        plt.xticks(rotation=30, ha="right")
    elif chart_type == "line":
        ax.plot(labels, values, marker="o", color="#2f6f6f")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        plt.xticks(rotation=30, ha="right")
    elif chart_type == "pie":
        ax.pie(values, labels=labels, autopct="%1.1f%%",
               colors=plt.cm.Set2.colors)
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

FROM python:3.11-slim

WORKDIR /app

# GPG anahtarı aramadan doğrudan kararlı FreeTDS sürücülerini kuruyoruz
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    tdsodbc \
    freetds-bin \
    freetds-dev \
    && rm -rf /var/lib/apt/lists/*

# ODBC ayar dosyasında FreeTDS sürücüsünü sisteme tanımlıyoruz
RUN echo "[FreeTDS]\nDescription=FreeTDS Driver\nDriver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\nSetup=/usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" > /etc/odbcinst.ini

EXPOSE 5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

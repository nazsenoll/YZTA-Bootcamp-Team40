# 1. Python taban imajı
FROM python:3.11-slim

# 2. Konteyner içi çalışma dizini
WORKDIR /app

# 3. Gerekli araçları, unixODBC'yi ve Microsoft SQL Sürücüsünü kuruyoruz
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    ca-certificates \
    unixodbc \
    unixodbc-dev \
    && curl -fsSL https://microsoft.com | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://microsoft.com > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends mssql-tools18 msodbcsql18 \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
    && rm -rf /var/lib/apt/lists/*

# 4. Flask uygulamasının dışarıdan erişilebilir olması için portu tanımlıyoruz
EXPOSE 5000

# 5. Bağımlılıkları kopyalayıp yüklüyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Proje dosyalarını kopyalıyoruz
COPY . .

# 7. Flask uygulamasını dış dünyaya açacak şekilde başlatıyoruz
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

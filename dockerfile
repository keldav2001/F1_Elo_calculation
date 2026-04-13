# Könnyűsúlyú Python alap
FROM python:3.10-slim

# Rendszer szintű frissítések és a JAVA telepítése a Spark miatt
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Munkakönyvtár beállítása a konténeren belül
WORKDIR /app

# Függőségek másolása és telepítése
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Dockerfile para aplicación PyQt5
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para PyQt5 y SQL Server
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    freetds-dev \
    freetds-bin \
    qt5-default \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5core5a \
    python3-pyqt5 \
    x11-apps \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements-pyqt5.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-pyqt5.txt

# Copiar el código de la aplicación
COPY . .

# Variables de entorno para Qt
ENV QT_X11_NO_MITSHM=1
ENV DISPLAY=:0

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
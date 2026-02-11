# =============================
# Dockerfile.prod (uv version)
# =============================

FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# -----------------------------
# Dependências do sistema
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg xvfb ca-certificates \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 \
    libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 \
    libnspr4 libnss3 libu2f-udev libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils \
    && rm -rf /var/lib/apt/lists/*


# -----------------------------
# Instala Google Chrome
# -----------------------------
RUN wget -q -O /usr/share/keyrings/google-linux-signing-keyring.gpg \
    https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*


# -----------------------------
# Instala ChromeDriver
# -----------------------------
RUN set -eux; \
    DRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE); \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip"; \
    unzip chromedriver-linux64.zip -d /tmp/; \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/; \
    chmod +x /usr/local/bin/chromedriver; \
    rm -rf /tmp/chromedriver-linux64* chromedriver-linux64.zip


# -----------------------------
# Instala UV
# -----------------------------
RUN pip install --no-cache-dir uv


# -----------------------------
# Variáveis
# -----------------------------
ENV CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


# -----------------------------
# Usuário não-root
# -----------------------------
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/temp && \
    chown -R appuser:appuser /app


WORKDIR /app


# -----------------------------
# Copia arquivos de deps
# (IMPORTANTE pro cache)
# -----------------------------
COPY pyproject.toml uv.lock ./


# -----------------------------
# Instala deps via uv
# -----------------------------
RUN uv sync --system --frozen


# -----------------------------
# Copia aplicação
# -----------------------------
COPY --chown=appuser:appuser grpa_backup/app ./


# -----------------------------
# TMP
# -----------------------------
RUN chmod 700 /app/temp

ENV TMPDIR=/app/temp


# -----------------------------
# User
# -----------------------------
USER appuser


# -----------------------------
# Healthcheck
# -----------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1


# -----------------------------
# Start
# -----------------------------
CMD ["python", "main.py"]

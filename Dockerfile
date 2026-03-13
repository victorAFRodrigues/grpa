# =============================
# Dockerfile
# =============================

FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instala uv
RUN pip install --no-cache-dir uv

# Copia deps primeiro (cache)
COPY pyproject.toml uv.lock ./

# Instala dependências
RUN uv sync --system --frozen

# Copia aplicação
COPY . .

# Diretório temporário
RUN mkdir -p /app/temp && chmod 700 /app/temp

ENV TMPDIR=/app/temp

# Healthcheck simples
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Executa seu main.py
CMD ["python", "main.py"]

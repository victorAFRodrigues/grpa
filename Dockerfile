FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instala uv
RUN pip install --no-cache-dir uv==0.10.2

# Copia deps primeiro (cache)
COPY pyproject.toml uv.lock ./

# Instala dependências
RUN uv sync --frozen

# Instala o browser e sua dependencias
RUN uv run playwright install-deps chromium
RUN uv run playwright install chromium

# Copia automations da imagem para backup
COPY automations /app/default_automations

# Copia aplicação
COPY . .

# Diretório temporário
RUN mkdir -p /app/temp && chmod 700 /app/temp

ENV TMPDIR=/app/temp

# Healthcheck simples
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Executa seu main.py
CMD ["uv", "run", "--active", "main.py"]

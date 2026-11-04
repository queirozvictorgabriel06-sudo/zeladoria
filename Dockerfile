FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


COPY Projeto/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY Projeto/ .


RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000


CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
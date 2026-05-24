FROM python:3.12-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# API code
COPY api/ .

# Static files (carte + data.json + api statique)
COPY docs/ /docs/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

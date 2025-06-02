FROM python:3.11-slim-buster as build
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./tmp/pyzdo_core-0.0.1.tar.gz /app/
RUN tar -xvf /app/*.tar.gz -C /app/. && \
  pip install /app/pyzdo_core-0.0.1/.

COPY src/ .
EXPOSE 8001

# CMD ["sh", "-c", "nginx -g 'daemon off;' & uvicorn main:app --host 0.0.0.0 --port 8001"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

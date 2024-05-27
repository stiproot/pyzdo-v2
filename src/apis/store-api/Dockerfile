FROM python:3.11-slim-buster as build

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./tmp/pm_common-0.0.1.tar.gz /app/
RUN tar -xvf /app/*.tar.gz -C /app/. && \
  pip install /app/pm_common-0.0.1/.

COPY src/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

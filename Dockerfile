FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
COPY ./alembic /alembic
COPY ./alembic.ini /alembic.ini

CMD bash -c "cd / && alembic upgrade head && cd /app && uvicorn main:app --host 0.0.0.0 --port 8080 --reload"

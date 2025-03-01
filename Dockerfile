FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
COPY ./alembic /alembic
COPY ./alembic.ini /alembic.ini

ENV PYTHONPATH=/

CMD bash -c "if [ \"$TEST_MODE\" = \"true\" ]; then \
	DATABASE_URL=mysql+asyncmy://user:password@db:3306/test_db alembic upgrade head && \
	pytest -v; \
  else \
	cd / && alembic upgrade head && cd /app && uvicorn main:app --host 0.0.0.0 --port 8080 --reload; \
  fi"

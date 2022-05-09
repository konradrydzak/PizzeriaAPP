FROM python:3.9-slim-buster

RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2

COPY ./src /src
COPY ./database.ini ./
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

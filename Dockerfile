FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

RUN apt-get update && apt-get install -y nodejs npm

RUN npm install --save fullcalendar

COPY . /app/

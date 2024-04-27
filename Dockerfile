# Używamy oficjalnego obrazu Pythona
FROM python:3.12

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik z zależnościami do katalogu roboczego
COPY pyproject.toml poetry.lock* /app/

# Instalujemy poetry
RUN pip install poetry

# Używamy poetry do instalacji zależności
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Kopiujemy resztę kodu do katalogu roboczego
COPY . /app/
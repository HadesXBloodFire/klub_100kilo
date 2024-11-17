# Klub 100 Kilo

### Wymagania wstępne:
- VPN lub połączenie z siecią AGH / użycie własnej bazy danych
- Zainstalowany Docker lub Poetry

## Jak włączyć aplikację?

1. Klonujemy repozytorium:
   ```sh
   git clone https://github.com/Davsooonowy/klub_100kilo.git
   cd klub_100kilo
   ```
## Wersja Dockerowa

Wchodzimy w katalog projektu i wywołujemy komendę: <br>
    ```
    docker-compose up --build
    ```

## Wersja z Poetry

Wchodzimy w katalog projektu i wywołujemy komendę:
    ```
    poetry install
    ```

Następnie uruchamiamy środowisko Poetry:
    ```
    poetry shell
    ```

Na koniec uruchamiamy serwer Django:
    ```
    Python3 manage.py runserver
    ```

## Aplikacja będzie dostępna pod adresem 
    http://localhost:8000/

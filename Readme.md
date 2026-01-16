# 🎓 School Gradebook API
Profesjonalny system elektronicznego dziennika szkolnego zbudowany w oparciu o framework FastAPI. Aplikacja umożliwia zarządzanie uczniami, kadrą pedagogiczną, ocenami oraz uwagami, oferując przy tym zaawansowane moduły raportowania i pełne bezpieczeństwo danych.

## 🚀 Główne Funkcjonalności

Zarządzanie Danymi (CRUD): Pełna obsługa uczniów, nauczycieli, przedmiotów, ocen oraz uwag.

Bezpieczeństwo: Autoryzacja oparta na protokole OAuth2 oraz tokenach JWT (JSON Web Tokens).

Relacje Wiele-do-Wielu: Zaawansowane mapowanie nauczycieli do wielu przedmiotów.

System Raportowania: Generowanie zestawień o uczniu (średnia ważona, punkty zachowania) z możliwością pobrania w formacie JSON lub XML.

Walidacja Danych: Restrykcyjna weryfikacja numerów PESEL oraz unikalności nazw przedmiotów.

Automatyczne Testy: Kompletny zestaw testów integracyjnych i jednostkowych (pytest).

## 🛠️ Stos Technologiczny
**Backend**: FastAPI

**Baza Danych**: MySQL (Obsługa asynchroniczna przez aiomysql)

**ORM**: SQLAlchemy 2.0 (Async)

**Bezpieczeństwo**: Jose (JWT), Passlib (Bcrypt)

**Testy**: Pytest & HTTPX

## 📋 Wymagania i Instalacja
1. Klonowanie i Środowisko


```` git clone <url-repozytorium>
cd projekt
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt 
````

2. Konfiguracja Zmiennych (.env)
Utwórz plik .env w głównym folderze i uzupełnij dane:

````
PROJECT_NAME="School Gradebook"
DATABASE_URL="mysql+aiomysql://użytkownik:hasło@localhost:3306/school_db"
SECRET_KEY="twój-bardzo-tajny-klucz"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
````

3. Inicjalizacja Bazy i Administratora
Aplikacja automatycznie tworzy tabele przy starcie. Aby utworzyć pierwszego użytkownika do logowania, uruchom:

````
python init_db.py
````
Domyślne dane: login: admin, hasło: admin123.

## 📖 Instrukcja Obsługi API
Uruchomienie serwera: uvicorn app.main:app --reload.

Dokumentacja interaktywna: Przejdź pod adres http://127.0.0.1:8000/docs.

Autoryzacja:

Użyj endpointu `/api/auth/login`, aby uzyskać token.

W interfejsie Swagger kliknij przycisk Authorize i wklej token, aby odblokować chronione ścieżki.

Raporty: Aby pobrać raport ucznia, wyślij żądanie GET `/api/reports/student/{id}/download?file_format=xml`.

## 🧪 Testowanie
System posiada zautomatyzowaną bazę testową, która tworzy się i czyści samoczynnie przy każdym uruchomieniu testów.

````
pytest
````

## 📂 Struktura Projektu
`app/api/`: Definicje tras (routes) oraz zależności.

`app/core/`: Konfiguracja i zabezpieczenia.

`app/crud/`: Logika operacji na bazie danych.

`app/models/`: Modele SQLAlchemy (Student, Teacher, Grade, Remark, User).

`app/schemas/`: Modele Pydantic do walidacji danych wejściowych/wyjściowych.

`tests/`: Testy funkcjonalne i fixture.
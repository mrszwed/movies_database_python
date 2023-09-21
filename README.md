# Projekt movies_database_python
Celem projektu było utworzenie aplikacji pozwalającej na wyszukiwanie informacji o filmach oraz osobach z nimi związanych zebranych w lokalnej bazie danych.
Zawartość danych odpowiada części bazy The Movie Database (https://www.themoviedb.org/?language=pl).

# Autor: Marcin Szwed

* pełne sprawozdanie znajduje się w katalogu documents w pliku movies-sprawozdanie.pdf
* kod tworzący bazę danych znajduje się w pliku creatable.txt w katalogu documents, znajduje się tam również diagram bazy danych (diagram.png)
* katalog model zawiera deklaracje klas odpowiadających encjom
* katalog feeding_db zawiera kod odpowiedzialny za pobieranie danych z TMDB API i zapis w bazie danych oraz raportowanie w plikach log przebiegu operacji
* katalog queries zawiera zapytania do bazy danych
* katalog web zawiera kod interfejsu użytkownika
* katalog natural_langauge zawiera kod odpowiedzialny za ładowani spacy (singleton) oraz kod defininujący wzorce zdań w języku naturalnym i ekstrakcję argumentów

![Zrzut ekranu 2023-09-21 153745](https://github.com/mrszwed/movies_database_python/assets/92521696/c2fec595-da65-4664-a5c1-8a0d1fda962a)

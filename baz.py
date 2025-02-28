import sqlite3
import json
import os

# Подключение к базе данных (или создание новой)
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Создание таблицы для фильмов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        year TEXT,
        rated TEXT,
        released TEXT,
        runtime TEXT,
        genre TEXT,
        director TEXT,
        writer TEXT,
        actors TEXT,
        plot TEXT,
        language TEXT,
        country TEXT,
        awards TEXT,
        poster TEXT,
        metascore TEXT,
        imdb_rating TEXT,
        imdb_votes TEXT,
        imdb_id TEXT UNIQUE,
        type TEXT,
        dvd TEXT,
        box_office TEXT,
        production TEXT,
        website TEXT,
        response TEXT
    )
''')

# Создание таблицы для рейтингов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        source TEXT,
        value TEXT,
        FOREIGN KEY (movie_id) REFERENCES movies (id)
    )
''')

# Путь к папке с JSON-файлами
movies_folder = 'bd\json-movie-list-master\movies'  # Укажите путь к папке movies из репозитория

# Проход по всем JSON-файлам
for filename in os.listdir(movies_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(movies_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            movie_data = json.load(file)

            # Вставка данных о фильме
            cursor.execute('''
                INSERT INTO movies (
                    title, year, rated, released, runtime, genre, director, writer,
                    actors, plot, language, country, awards, poster, metascore,
                    imdb_rating, imdb_votes, imdb_id, type, dvd, box_office,
                    production, website, response
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                movie_data.get('Title'),
                movie_data.get('Year'),
                movie_data.get('Rated'),
                movie_data.get('Released'),
                movie_data.get('Runtime'),
                movie_data.get('Genre'),
                movie_data.get('Director'),
                movie_data.get('Writer'),
                movie_data.get('Actors'),
                movie_data.get('Plot'),
                movie_data.get('Language'),
                movie_data.get('Country'),
                movie_data.get('Awards'),
                movie_data.get('Poster'),
                movie_data.get('Metascore'),
                movie_data.get('imdbRating'),
                movie_data.get('imdbVotes'),
                movie_data.get('imdbID'),
                movie_data.get('Type'),
                movie_data.get('DVD'),
                movie_data.get('BoxOffice'),
                movie_data.get('Production'),
                movie_data.get('Website'),
                movie_data.get('Response')
            ))

            # Получение ID последнего вставленного фильма
            movie_id = cursor.lastrowid

            # Вставка рейтингов
            for rating in movie_data.get('Ratings', []):
                cursor.execute('''
                    INSERT INTO ratings (movie_id, source, value)
                    VALUES (?, ?, ?)
                ''', (movie_id, rating.get('Source'), rating.get('Value')))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
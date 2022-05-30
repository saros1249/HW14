import sqlite3


class Dbdata:

    def __init__(self, path):
        self.path = path

    def load_data(self):
        """
        Создаёт соединение с БД.
        """
        return sqlite3.connect(self.path)

    def search_by_title(self, search_title):
        """
        Поиск по названию фильма
        :param search_title: Название
        :return: Словарь.
        """
        connection = self.load_data()
        cursor = connection.cursor()
        sqlite_query = f"""SELECT title, country, MAX(release_year), listed_in, description
                          FROM netflix
                          WHERE title LIKE '%{search_title}%'
                       """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        connection.close()
        return {"title": data[0][0],
                "country": data[0][1],
                "release_year": data[0][2],
                "genre": data[0][3],
                "description": data[0][4]}

    def search_by_release_years(self, years_min, years_max):
        """
        Поиск по диапазону годов выхода фильма.
        :param years_min:
        :param years_max:
        :return: Список словарей.
        """
        connection = self.load_data()
        cursor = connection.cursor()
        sqlite_query = f"""SELECT title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN {years_min} AND {years_max}
                        ORDER BY release_year LIMIT 100
                        """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        connection.close()
        data_list = []
        for i in range(len(data)):
            data_list.append({"title": data[i][0],
                              "release_year": data[i][1]})
        return data_list

    def search_by_rating(self, rating):
        """
        Поиск по рейтингу фильма.
        :param rating:
        :return: Список словарей.
        """
        rating_parameters = {
            "children": "'G'",
            "family": "'G', 'PG', 'PG-13'",
            "adult": "'R', 'NC-17'"
        }
        if rating not in rating_parameters:
            return 'Данные для поиска указаны не корректно'
        connection = self.load_data()
        cursor = connection.cursor()
        sqlite_query = f"""SELECT title, rating, description
                        FROM netflix
                        WHERE rating in ({rating_parameters[rating]})
                        """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        connection.close()
        data_list = []
        for i in range(len(data)):
            data_list.append({"title": data[i][0],
                              "rating": data[i][1],
                              "description": data[i][2]})
        return data_list

    def top_films_by_genre(self, genre):
        """
        Поиск по жанру.
        :param genre:
        :return: Список словарей.
        """
        connection = self.load_data()
        cursor = connection.cursor()
        sqlite_query = f"""SELECT title, description
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%'
                        ORDER BY release_year DESC
                        """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        connection.close()
        data_list = []
        for i in range(len(data)):
            data_list.append({"title": data[i][0],
                              "description": data[i][1]})
        return data_list


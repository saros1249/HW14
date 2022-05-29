import sqlite3


class Dbdata:

    def __init__(self, path):
        self.path = path

    def load_data(self):
        return sqlite3.connect(self.path)

    def search_by_title(self, search_title):
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
        rating_parameters = {
            "children": "'G'",
            "family": "'G', 'PG', 'PG-13'",
            "adult": "'R', 'NC-17'"
        }
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

    def colleagues(self, a, b):
        connection = self.load_data()
        cursor = connection.cursor()
        sqlite_query = f"""SELECT `cast`
                        FROM netflix
                        WHERE `cast` LIKE '%{a}%' 
                        AND `cast` LIKE '%{b}%'
                        """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        connection.close()

        data_list = []
        colleagues_list = []

        for i in range(len(data)):
            l = data[i][0].split(', ')
            data_list.extend(l)

        for i in range(len(data_list)):
            if data_list.count(data_list[i]) > 2:
                colleagues_list.append(data_list[i])

        total_set = set(colleagues_list)

        total_set.remove(a)
        total_set.remove(b)

        return total_set

    def search_by_type_year_genre(self, type, year, genre):
        connection = self.load_data()
        cursor = connection.cursor()
        sqlite_query = f"""SELECT title, description
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%' 
                        AND type = '{type}'
                        AND release_year = '{year}'
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
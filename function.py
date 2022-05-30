import sqlite3


def colleagues(actor_1, actor_2):
    """
    Поиск коллег для двух актеров, которые снимались совместно более 2-х раз.
    :return: Множество.
    """
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    sqlite_query = f"""SELECT `cast`
                    FROM netflix
                    WHERE `cast` LIKE '%{actor_1}%' 
                    AND `cast` LIKE '%{actor_2}%'
                    """
    cursor.execute(sqlite_query)
    data = cursor.fetchall()
    connection.close()

    data_list = []
    colleagues_list = []

    for i in range(len(data)):
        data_list.extend(data[i][0].split(', '))

    for i in range(len(data_list)):
        if data_list.count(data_list[i]) > 2:
            colleagues_list.append(data_list[i])

    total_set = set(colleagues_list)

    total_set.remove(actor_1)
    total_set.remove(actor_2)

    return total_set


def search_by_type_year_genre(type, year, genre):
    """
    Поиск по типу, году выхода, жанру.
    :return: Список словарей.
    """
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    sqlite_query = f"""SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%' 
                    AND type = '{type}'
                    AND release_year = {year}
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

print(colleagues('Jack Black', 'Dustin Hoffman'))
print(search_by_type_year_genre('Movie', 2019, 'Thrillers'))
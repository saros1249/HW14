from flask import Flask, jsonify

from utils import Dbdata

dbdata = Dbdata('netflix.db')

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False


@app.route('/movie/<title>/')
def search_movie_by_title(title):
    return dbdata.search_by_title(title)


@app.route('/movie/<int:year_1>/to/<int:year_2>')
def search_movie_by_year(year_1, year_2):
    return jsonify(dbdata.search_by_release_years(year_1, year_2))


@app.route('/rating/<rating>')
def search_by_rating(rating):
    return jsonify(dbdata.search_by_rating(rating))


@app.route('/genre/<genre>')
def search_by_genre(genre):
    return jsonify(dbdata.top_films_by_genre(genre))


if __name__ == '__main__':
    app.run(debug=True)

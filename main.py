import requests
import sqlite3
import config as cfg


root = "https://api.themoviedb.org/3"
root2 = "https://api.themoviedb.org/4"

genres = "/genre/movie/list"
mylist = f"/list/{cfg.mylist}"
rated_movie = f"/account/{cfg.account_id}/movie/rated"

# connect db
con = sqlite3.connect('movies.db')
cur = con.cursor()
# reset table
cur.execute("DROP TABLE IF EXISTS movies")
cur.execute(
    """
    CREATE TABLE movies (
        id, release_date, title, original_title, genres, vote_average, my_rating, poster_path, overview
    )
    """
)
# create session
s = requests.Session()

# get genres
r = s.get(root+genres, params=dict(
    api_key=cfg.api_key,
    language=cfg.locale
))
gen = r.json()
gen_dict = dict()
for g in gen.get("genres"):
    gen_dict[g['id']] = g['name']

# get rated movies
ratings = dict()
page = 1
while True:
    r = s.get(
        root2+rated_movie,
        headers={
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": f"Bearer {cfg.read_access_token}"
        },
        params={
            'page': page
        }
    )
    data = r.json()
    for res in data.get('results'):
        ratings[res['id']] = res['account_rating']['value']
    page += 1
    if page > data.get('total_pages', 0):
        break

# get movie list
page = 1
while True:
    r = s.get(
        root2+mylist, 
        params=dict(
            api_key=cfg.api_key,
            sort_by="primary_release_date.desc",
            language=cfg.locale,
            page=page
        ),
        headers={
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": f"Bearer {cfg.read_access_token}"
        },
    )
    data = r.json()
    for x in data.get('results'):
        id = x.get('id')
        media_type = x.get('media_type')
        if media_type != 'movie':
            continue
        release_date = x.get('release_date')
        title = x.get('title')
        original_title = x.get('original_title')
        genre_ids = x.get('genre_ids')
        genres = ";".join([gen_dict.get(y) for y in genre_ids])
        vote_average = x.get('vote_average')
        poster_path = x.get('poster_path')
        overview = x.get('overview')
        my_rating = ratings.get(id)
        cur.execute("insert into movies values (?,?,?,?,?,?,?,?,?)", (id, release_date, title, original_title, genres, vote_average, my_rating, poster_path, overview))
    page += 1
    if page > data.get('total_pages', 0):
        break
con.commit()
con.close()
import config as cfg
import sqlite3
from jinja2 import Environment, FileSystemLoader
from itertools import zip_longest

def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def format_date(st):
    if not st:
        return ''
    return '/'.join([st[8:10], st[5:7], st[:4]])

# load template
env = Environment(loader=FileSystemLoader(cfg.template_root))
temp = env.get_template("template.html")

# connect db
con = sqlite3.connect('movies.db')
cur = con.cursor()

# custom query
cur.execute(
    """
    select 
    id, release_date, title, original_title, genres, vote_average, my_rating, poster_path, overview 
    from movies
    where 
    --genres like '%Thriller%'
    --and 
    my_rating is null
    order by vote_average desc
    """
)
res = cur.fetchall()
data_b = list()
for id, release_date, title, original_title, genres, vote_average, my_rating, poster_path, overview in res:
    data_b.append(
        dict(
            id=id,
            release_date=format_date(release_date),
            title=title,
            original_title=original_title,
            genres=genres.split(';'),
            vote_average=vote_average,
            my_rating=my_rating ,
            poster_path=poster_path,
            overview=overview
        )
    )

data = grouper(6, data_b)

html_content = temp.render(movies=data)
with open('results.html', 'w', encoding='utf8') as f:
    f.write(html_content)

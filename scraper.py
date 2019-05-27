from bs4 import BeautifulSoup
import requests
import re
import pymongo
import traceback

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['imdb']
mycol = mydb['movies']


url = 'https://www.imdb.com/list/ls006266261/?sort=list_order,asc&st_dt=&mode=detail&page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

movies_ids = []
movie_details = {}

for i in soup.select('div.lister-item-image.ribbonize'):
    id = i.attrs.get('data-tconst')
    movies_ids.append(id)
    movie_details[id] = {'_id':id}

for key in movie_details.keys():
    director = soup.select('p.text-muted.text-small a')[0].contents[0].strip()
    url_2 = 'https://www.imdb.com/title/'+key
    soup_2 = BeautifulSoup(requests.get(url_2).text, 'html.parser')
    name = soup_2.select('div.title_wrapper h1')[0].contents[0].strip()
    release_year = soup_2.select('div.title_wrapper h1 a')[0].contents[0].strip()
    briefs = soup_2.select('div.summary_text')[0].contents[0].strip()
    cast_list = soup_2.select('table.cast_list tr td a')
    cast = []
    try:
        for i in range(0,len(cast_list),3):
            actor = cast_list[i+1].contents[0].strip()
            character = cast_list[i+2].contents[0].strip()
            cast.append({'actor':actor,'character':character})
        print(cast)
    except Exception as e:
        print(key,e)
    rating = soup_2.select('div.ratingValue strong span')[0].contents[0].strip()
    movie_details[key]['name'] = name
    movie_details[key]['release_year'] = release_year
    movie_details[key]['rating'] = rating
    movie_details[key]['director'] = director
    movie_details[key]['briefs'] = briefs
    movie_details[key]['cast'] = cast

insertion = []
for i,j in movie_details.items():
    insertion = mycol.insert_one(j)

if insertion.inserted_id is not None:
    print('Movies added to database.')

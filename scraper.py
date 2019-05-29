from bs4 import BeautifulSoup, Tag, NavigableString
import requests
import re
import pymongo
import traceback
import time


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['imdb']
mycol = mydb['movies']

movies_count = 0
full_start = time.time()
all_movie_details = {}

for m in range(1,11):
    stage_start = time.time()

    print(f'Stage {m}:')
    url = 'https://www.imdb.com/list/ls006266261/?sort=list_order,asc&st_dt=&mode=detail&page='+str(m)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies_ids = []
    movie_details = {}

    for i in soup.select('div.lister-item-image.ribbonize'):
        # Adding movie ids in list & dictionary to further scrap movie wise
        id = i.attrs.get('data-tconst')
        movies_ids.append(id)
        movie_details[id] = {'_id':id}

    for key in movie_details.keys():
        # Time taken
        start = time.time()

        # Scraping code
        url_2 = 'https://www.imdb.com/title/'+key
        soup_2 = BeautifulSoup(requests.get(url_2).text, 'html.parser')
        name = soup_2.select('div.title_wrapper h1')[0].contents[0].strip()

        # Since there can be tv series as well so checking for movie or tv series
        try:
            release_year = soup_2.select('div.title_wrapper h1 a')[0].contents[0].strip()
        except Exception:
            release_year = '-'

        briefs = soup_2.select('div.summary_text')[0].contents[0].strip()
        rating = soup_2.select('div.ratingValue strong span')[0].contents[0].strip()
        director = soup_2.select('div.credit_summary_item a')[0].contents[0].strip()

        cast = []
        cast_list = soup_2.select('table.cast_list tr td')
        # Eliminating labels and image and choosing character and actor in cast table
        pair_count = 0
        actor = ''
        character = ''
        for i in range(len(cast_list)):
            if cast_list[i].attrs.get('class') is None:
                # Filtering if there is any other unnecessary field with no class
                try:
                    actor = cast_list[i].select('a')[0].contents[0].strip()
                except Exception:
                    pass
            elif cast_list[i].attrs.get('class')[0] == 'character':
                try:
                    character = cast_list[i].select('a')[0].contents[0].strip()
                except Exception:
                    character = cast_list[i].contents[0].strip()
            if actor != '' and pair_count == 0:
                # print('actor',actor,end=' : ')
                pair_count += 1
            if character != '' and pair_count == 1:
                # print('character',character)
                pair_count += 1
            if pair_count == 2:
                cast.append({'actor':actor,'character':character})
                pair_count = 0
                actor = ''
                character = ''

        # Filling all data in dictionary to upload in DB
        movie_details[key]['name'] = name
        movie_details[key]['release_year'] = release_year
        movie_details[key]['rating'] = rating
        movie_details[key]['director'] = director
        movie_details[key]['briefs'] = briefs
        movie_details[key]['cast'] = cast

        # Updating movies count
        movies_count += 1

        # Time taken
        end = time.time()

        # Notifier of data fetch
        print(f'Data fetched of movie {movies_count} , id : {key} , time {end - start}')

    stage_end = time.time()
    all_movie_details.update(movie_details)
    print(f'Stage {m} completed in time: {stage_end - stage_start}')

confirm = input('Do you want to save this data in database?(Y/N)')
if confirm in 'Yy':
    print('Inserting in database........')
    inserting_data = []
    data_count = 0

    # Appending all data in one to insert in a single go
    for i,j in movie_details.items():
        inserting_data.append(j)
        data_count += 1

    insertion = mycol.insert_many(inserting_data)

    if len(insertion.inserted_ids) == data_count:
        print('All movies added to database.')
    else:
        print('Some movies could not be added to database.')

full_end = time.time()
print(f'Scraping completed in time: {full_end - full_start}')

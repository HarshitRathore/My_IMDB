from bs4 import BeautifulSoup
import requests
import re
import pymongo
import traceback

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
    url_2 = 'https://www.imdb.com/title/tt0099685/'
    soup_2 = BeautifulSoup(requests.get(url_2).text, 'html.parser')
    cast_list = soup_2.select('table.cast_list tr td')
    cast = []
    for i in range(1,len(cast_list),4):
        actor = cast_list[i+1].contents[1].contents[0].strip()
        for j in cast_list[i+3].contents:
            if j != '\n':
                print(j)
        # character = cast_list[i+3].contents[1].contents[0].strip()
        # cast.append({'actor':actor,'character':character})
        # print(cast)
    break
    # cast = []
    # try:
    #     for i in range(0,len(cast_list),3):
    #         actor = cast_list[i+1].contents[0].strip()
    #         character = cast_list[i+2].contents[0].strip()
    #         cast.append({'actor':actor,'character':character})
    #         print(cast)
    # except Exception as e:
    #     print(key,e)
    #     traceback.print_exc()
    break

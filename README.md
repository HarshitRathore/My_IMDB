# My_IMDB

It is a full stack project which do scrapping form the the imdb site 
and scrapes 1000 greatest movies and then stores it in MongoDB
and then show it on web app ,which is developed with Flask API and Bootstrap/React Framework.


# Pre-Requisites

1. MongoDB must be well established on your PC and well connected .
2. For React npm must installed.
3. Python 3.7 must also be present.

# Installation
1. Install the libraries of python from requirements.txt file 

	 `pip -r requirements.txt`

# How to run the Project ( Usage )
1. Scrap the site 

    `python scrapper.py`
    
	(caution: if in case scrapper stops in  middle then delete all the incomplete 	database from mongodb )
   ***average scrapping time(30 min ,depends on the internet and cpu) ***

2. Now start the flask server 

	`cd flask_api` 
  
	`python my_imdb.py` 

3. Now if you want to run the Bootstrap Front-End then go to Bootstrap folder and run index.html
4. If you want to run React Front-End then

	`cd react_my_imdb`
  
	`npm -i`
  
	`npm start`  


# test_tmdb

Run main to fetch movie infos for all the movies in the list, saves it to a sqlite db

Edit the sql query and run fill_template to query the db and generate html page with the results

## install
Create a config.py file with:  
api_key, read_access_token -> https://www.themoviedb.org/settings/api  
account_id -> your account id  
mylist -> id of the list to fetch  
locale -> fr-FR, en-GB ...  
template_root -> path to template folder

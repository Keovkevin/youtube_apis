# youtube_apis
To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

# Basic Requirements
- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- A basic search API to search the stored videos using their title and description.
- Dockerize the project.
- It should be scalable and optimised.

# References
- YouTube data v3 API: [https://developers.google.com/youtube/v3/getting-started](https://developers.google.com/youtube/v3/getting-started)
- Search API reference: [https://developers.google.com/youtube/v3/docs/search/list](https://developers.google.com/youtube/v3/docs/search/list)
    - To fetch the latest videos you need to specify these: type=video, order=date, publishedAfter=<SOME_DATE_TIME>
    - Without publishedAfter, it will give you cached results which will be too old

# Database configuration
python3 -m venv env

source env/bin/activate

install mysql the start the service

install mysql workbench

## Rescan servers: It finds the running MySQL instance and saves that connection in the MySQL connections area

1.Click the Schema tab

2.Right-click in the Schema list and select Create Schema

3.Give it a name and follow the prompts to create it

## Set up db user

1.Select the Administration tab

2.Select Users and Privileges

3.Click Add Account

4.Give your user a name and password

5.Assign Administrative Roles and Schema Privileges

## install mysql client

## Open settings.py for the Django project

By default, you’ll see that it is configured to use SQLite

Update the connection string following the example below. Use your own values for Name (this is the schema created earlier), User, Password and Port (you can find the port from Server Status in the Administration tab if needed).

DATABASES = {
    ‘default’: {
        ‘ENGINE’: ‘django.db.backends.mysql’,
        ‘NAME’: ‘sunforge’,
        ‘USER’: ‘dbadmin’,
        ‘PASSWORD’: ‘password’,
        ‘HOST’: ‘127.0.0.1',
        ‘PORT’: ‘3306',
    }
}

python manage.py migrate

You should see it reporting in the terminal that it is migrating tables for all the INSTALLED_APPS.

# Installing Redis
1.curl -O http://download.redis.io/releases/redis-5.0.5.tar.gz 

2.tar xzf redis-5.0.5.tar.gz

3.cd redis-5.0.5

4.make

To Run the server: "src/redis-server"

# pip install -r requirements.txt

# Enabling redis server and using celery worker and beat
src/redis-server

python manage.py runserver

celery -A app_name worker -l info

celery -A app_name beat -l info

# Need to check YOUTUBE_API_KEYS and query to extract data

# adding postman collection for url and payload definition : https://www.getpostman.com/collections/1573e12927edce8631a6

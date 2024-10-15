# Media Inventory Tracking System

MITS is designed to provide you a filtered read-only view of your Jellyfin library in a simple, mobile friendly UI.

## Description

This project was designed to help me with buying new movies and TV Shows and keep track of the movies that I purchased on Jellyfin.  When I'm out and see a good price at the store, but can't remember if I own it yet (or what format) I want an easy way to view what I own.  By leveraging Python and the Jellyfin API, I came up with a solution that works for me and may be of use for others - or at least provide examples on how to integrate with Jellyfins API.  Note that previously I used NFO files but found it problematic.. I've left the nfo.py file in for anyone curious to look at it.

This project allows me to track only movies I bought that are stored in certain directories (useful if you have a mix of digital available only vs physical discs) and by leveraging tags allows me to see what format I own them on.  In my case by default if no DVD or 4K aren't found it defaults to Blu-ray, but can be customized to suit your needs.

This very much is for my niche purposes but sharing in case anyone else has the need / perhaps the Jellyfin API code can be used as examples.

### Features

Mobile first UI
* Basic login for a single user - Although there is some simple authentication, this app should not be considered secure and is best placed behind something like a VPN.  Python isn't my day job so its likely I've made mistakes.
* Card view and sortable List view
* Search
* Filter by media type (Movies/Series) and monitored Tags
* Limit scanning to specified directories - useful if you only want to include a subset of your library
* Automatically uses Jellyfins cover art, and provides links to TMDB and IMDb.
* Fairly customizable - see the .env file explanation below
* Series with multiple Seasons are tracked by Season - so if you have only bought certain seasons, only those will show up.

## Getting Started

### Dependencies

* Jellyfin - won't work without it!
* Docker Compose is highly recommended (docker compose provided below)
* No art work is included, you will likely want to add the following files to "images/icons" and make it more purty:
  * imdb.png - button to open the IMDb page for the movie/tv show
  * tmdb.png - button to open the TMDB page for the movie/tv show
  * mits.png - app icon
  * default.png - if no tags are found, this will be displayed
  * tag-name.png - where tag-name is the name of the tag you want to monitor for (i.e. DVD, Blu-ray, 4k, etc) 
* Note that I run this on Docker Compose with Portainer as the UI to manage - Linux based server.

### Installing

* create a docker compose file similar to below

```
services:
  app:
    image: redpanda464/mits
    volumes:
      - /path_to_mits_images:/python_app/static/images
    depends_on:
      - redis
    working_dir: /python_app
    ports:
      - "${APP_PORT}:${APP_PORT}"  # Map container port to host port, set this in the .env file below
    command: gunicorn --config gunicorn_config.py main:app
    restart: unless-stopped
    env_file:
      .env #comment out if using portainers stack.env file below
      .secrets #comment out if using portainers stack.env file below
      #stack.env #if using portainers env uncomment this 
  redis: #this must match REDIS_SERVER_NAME
    image: redis:alpine
    ports:
      - "${REDIS_PORT}:${REDIS_PORT}" # Map container port to host port, set this in the .env file below
    volumes:
      - /path_to_redis_directory:/data  # Mount a named volume for persisting data  
    environment:
      REDIS_ARGS: --save 600 1
    working_dir: /data
    restart: unless-stopped

volumes:
  # Additional volumes for shared data
  redis-data:  # Define a named volume for persistence
```

* modify your .env file to match your environment:

```
MOVIE_WATCH_DIRS='["", ""]'    #this is an array of folders - if the Path in jellyfin doesn't match what you have here, that Title is ignored
SERIES_WATCH_DIRS='["", ""]'   #this is an array of folders - if the Path in jellyfin doesn't match what you have here, that Title is ignored
LIBRARIES='["Movies", "TV Shows", "Anime"]' #what Libraries to monitor
JELLYFIN_URL='http://jellyfin_ip_address/optional_sub_to_jelly/' #location of your jellyfin instance 
TAG_WATCH='["DVD", "4K", "Blu-Ray"]' #which tags we care about - if we see the matching tag on scan, we'll add and display that in MITS
TAG_DEFAULT='Blu-Ray' #if no matching tags are found, apply this tag.  Useful so you only have to update the exceptions
SEASON_IGNORE='["Specials"]'  #ignore any special seasons you wouldn't normally buy (such as specials included in each season)
EXCLUDE_LOCATION_TYPES='Virtual' #Jellyfin will add empty seasons to shows you only own part of - this will ensure those are ignored
APP_PORT=8092 #port of MITS
REDIS_SERVER_NAME=redis
REDIS_PORT=6379
GUNICORN_BIND='0.0.0.0'
```

* secrets are customized in the .secrets file (stored in clear text for now - beware!)
```SESSION_SECRET="session_secret_random" #random characters for handling user authentication 
USERNAME="mits" #name of the user 
PASSWORD="CustomPasswordGoesHere" #password
JELLYFIN_API_KEY="jellyfin_api"SESSION_SECRET="session_secret_random" #API key from Jellyfin
```

### Executing program

Once the container is loaded, you can view the app by going to http://server_name:app_port_number (https is best managed via something like nginx)

## Authors

[Terence-D](https://github.com/Terence-D)

## Version History

* 1.0
    * Initial Release

## License

This project is licensed under the Apache-2.0 License - see the LICENSE.md file for details

## Acknowledgments

Shout out to Jellyfin for its great API!

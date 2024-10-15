import os
import json 

#extract environment variables
movieFolders = json.loads(os.environ.get('MOVIE_WATCH_DIRS', '["/media/Movies"]'))
seriesFolders = json.loads(os.environ.get('SERIES_WATCH_DIRS', '["/media/Series"]'))
watchedTags = json.loads(os.environ.get('TAG_WATCH', '["DVD", "4K", "Blu-Ray"]'))
seasonsToIgnore = json.loads(os.environ.get('SEASON_IGNORE', '["Specials"]'))
defaultTag = os.environ.get('TAG_DEFAULT', 'Blu-Ray')
moviePrefix = "MOVIE-"
seriesPrefix = "SERIES-"

class Media:
    def __init__(self, title = "", year = "", imdb = "", tmdb = "", id = "", poster = "", tags = []):
        self.title = title
        self.year = year
        self.imdb = imdb
        self.tmdb = tmdb
        self.poster = poster
        self.tags = tags 
        self.id = id
    def getUniqueId(self):
        if hasattr(self, "seasons"):
            return seriesPrefix + self.id
        return moviePrefix + self.id

class Season:
    def __init__(self, year = "", poster = "", seasonTitle = "", tags = []):
        self.seasonTitle = seasonTitle
        self.year = year
        self.tags = tags 
    def getUniqueId(self):
        return seriesPrefix + self.seasonTitle + self.year

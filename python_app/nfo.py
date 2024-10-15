import os
import glob
import xml.etree.ElementTree as ET
import mitsCommon
import mitsData
import shutil

from pathlib import Path
from datetime import datetime

def updateAllNfos(fullRefresh = True):
    then = datetime.now()        # Random date in the past

    if (fullRefresh):
        print ("full refresh in progress")
    else:
        print ("partial refresh in progress")

    getSeriesNfos(fullRefresh)
    files = getMovieNfos()
    generateMovieNfoData(files, fullRefresh)

    now  = datetime.now()                         # Now
    duration = now - then                         # For build-in functions
    duration_in_s = duration.total_seconds()  
    print("Operation took ", duration_in_s, " seconds.")

def getSeriesNfos(fullRefresh = True):
    foundKeys = []
    files = []
    for watchFolder in mitsCommon.seriesFolders:
        for dirPath, dirNames, filenames in os.walk(watchFolder):
            for filename in [f for f in filenames if f == "tvshow.nfo"]:
                tvShowPath = (os.path.join(dirPath, filename))
                series = generateSeriesNfoData(tvShowPath, fullRefresh)
                series.seasons = []
                for seasonPath, seasonPathnames, seasonFilenames in os.walk(dirPath):
                    for seasonFilename in [f for f in seasonFilenames if f == "season.nfo"]:
                        season = generateSeasonNfoData(os.path.join(seasonPath, seasonFilename))
                        if season.seasonTitle not in mitsCommon.seasonsToIgnore:
                            series.seasons.append (season)
                if mitsData.add(series, fullRefresh):
                    foundKeys.append (series.getUniqueId())
    if (fullRefresh):
        mitsData.remove(foundKeys, mitsCommon.seasonPrefix)
    return files

def getMovieNfos():
    files = []
    for dir in mitsCommon.movieFolders:
        # Search for files with a specific extension (e.g., .txt)
        files +=  glob.glob(os.path.join(dir, '**/*.nfo'), recursive=True)
    return files

def generateSeasonNfoData(file):
    media = mitsCommon.Season()
    try:
        # Parse an XML file
        tree = ET.parse(file)
        root = tree.getroot()

        media.seasonTitle = getElementText(root, 'title')
        media.year = getElementText(root, 'year')
        media.poster = getElementText(root, 'poster', 'art')

        media.tags = []
        for tagElement in root.findall('tag'):
            for tag in mitsCommon.watchedTags:
                if tag.lower() == tagElement.text.lower():
                    media.tags.append(tag)

    except Exception as e:
        print ("error parsing season xml for " + file + " " + str(e))
    return media

def generateSeriesNfoData(file, fullRefresh = True):
    media = mitsCommon.Series()
    try:
        # Parse an XML file
        tree = ET.parse(file)
        root = tree.getroot()

        media.title = getElementText(root, 'title')
        media.year = getElementText(root, 'year')
        media.imdb = getElementText(root, 'imdbid')
        media.tmdb = getElementText(root, 'tmdbid')
        media.poster = getElementText(root, 'poster', 'art')
        media.poster = mitsCommon.copyImage(media.poster, media.getUniqueId(), file, fullRefresh)
        media.tags = [] #for cases like anime
        for tagElement in root.findall('tag'):
            for tag in mitsCommon.watchedTags:
                if tag.lower() == tagElement.text.lower():
                    media.tags.append(tag)
    except Exception as e:
        print ("error parsing series xml for " + file + " " + str(e))
    return media

def generateMovieNfoData(files, fullRefresh = True):
    foundKeys = []
    for file in files:
        try:
            # Parse an XML file
            tree = ET.parse(file)
            root = tree.getroot()
            media = mitsCommon.Movie()
            media.title = getElementText(root, 'title')
            media.year = getElementText(root, 'year')
            media.imdb = getElementText(root, 'imdbid')
            media.tmdb = getElementText(root, 'tmdbid')
            
            media.poster = getElementText(root, 'poster', 'art')
            media.poster = mitsCommon.copyImage(media.poster, media.getUniqueId(), file, fullRefresh)

            media.tags = []
            for tagElement in root.findall('tag'):
                for tag in mitsCommon.watchedTags:
                    if tag.lower() == tagElement.text.lower():
                        media.tags.append(tag)

            if mitsData.add(media, fullRefresh):
                foundKeys.append (media.getUniqueId())
        except Exception as e:
            print ("error parsing movie xml for " + file + " " + str(e))
    if (fullRefresh):
        mitsData.remove(foundKeys, mitsCommon.mediPrefix)

def getElementText(root, text, subfolder = ''):
    try:
        element = None
        if subfolder != '':
            element = root.find(subfolder).find(text)
        else:
            element = root.find(text)
        if element is not None:
            return element.text
        else:
            return "-"
    except Exception as e:
        print ("error finding " + text + " " + str(e))
    return "-"

def copyImage(source, key, nfoFile, fullRefresh = True): 
    destination = "/python_app/static/images/media/" + key + ".jpg"

    destinationFile = Path(destination)

    pathToCheck = Path(source)    
    if pathToCheck.is_file():
        if destinationFile.is_file() == False or fullRefresh:
            shutil.copy(source, destination)
        else:
            print (destination + " file already exists , skipping")
        return source
    else: 
        #file doesn't exist, try looking for a default folder icon
        path = os.path.dirname(nfoFile)
        backFile = str(path) + '/folder.jpg'
        pathToCheck = Path(backFile)    
        if pathToCheck.is_file():
            if destinationFile.is_file() == False or fullRefresh:
                shutil.copy(backFile, destination)
            else:
                print (destination + " file already exists , skipping")
            return backFile
        else:
            #if nothing, then we don't get an image.  shucks
            return ""

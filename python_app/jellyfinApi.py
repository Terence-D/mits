import requests
import json
import mitsCommon
import mitsData
import os

# Replace with the actual API URL you want to access
apiBaseUrl = os.environ.get('JELLYFIN_URL')
endpointLibraries = f"{apiBaseUrl}Library/MediaFolders"
endpointLibraryItems = f"{apiBaseUrl}Items/?parentId={{}}&fields=path,tags,externalUrls"
endpointImages = f"{apiBaseUrl}Items/{{}}/Images/primary"

# Replace with your actual media browser token
apiKey = os.environ.get('JELLYFIN_API_KEY')
authToken = f'MediaBrowser Token="{apiKey}"'
excludeLocationTypes = os.environ.get('EXCLUDE_LOCATION_TYPES')

# Set the authorization header
headers = {"Authorization": f"{authToken}"}

Libraries = json.loads(os.environ.get('LIBRARIES', '["Movies", "TV Shows"]'))

def readImage(id, key):
  endpoint = endpointImages.format(id)
  imageResponse = requests.get(endpoint, headers=headers)
  if (imageResponse.status_code == 200):
    filename = key + ".jpg"
    directory = "/python_app/static/images/media/" 
    if not os.path.exists(directory):
      os.makedirs(directory) # Create the directory if it does not exist
    filePath = os.path.join(directory, filename)
    with open(filePath, "wb") as f:
      f.write(imageResponse.content)
    return filename
  else:
    print(f"API request failed with status code: {imageResponse.status_code}")

def readMediaLibrary(id, fullRefresh, isSeries):
  endpoint = endpointLibraryItems.format(id)
  if excludeLocationTypes != '':
    endpoint += "&excludeLocationTypes=" + excludeLocationTypes

  libraryResponse = requests.get(endpoint, headers=headers)
  libraryData = json.loads(libraryResponse.text)
  libraryItems = libraryData["Items"]

  foundKeys = []

  folder = mitsCommon.movieFolders
  if (isSeries):
    folder = mitsCommon.seriesFolders

  for item in libraryItems:
    if startsWithAny(item["Path"], folder):
      media = mitsCommon.Media()
      media.title = item["Name"]
      
      # Check if "ProductionYear" exists in the item dictionary
      if "ProductionYear" in item:
          media.year = item["ProductionYear"]
      else:
          # print (media.title)
          # for key in item.keys(): print(key)
          # Handle the case where the key doesn't exist
          media.year = "UNKOWN"  # or any default value you prefer

      if "ExternalUrls" in item:
        urls = item["ExternalUrls"]
        for url in urls:
          if url["Name"] == "IMDb":
            media.imdb = url["Url"]
          if url["Name"] == "TheMovieDb":
            media.tmdb = url["Url"]
      
      media.id = item["Id"]
      if (isSeries):
        media.seasons = generateSeasons(media.id, media.title)
      else:
        media.tags = getTags(item)

      media.poster = readImage(item["Id"], media.getUniqueId())

      if mitsData.add(media, fullRefresh):
        foundKeys.append (media.getUniqueId())

  return foundKeys

def getTags(item):
  foundTags = []
  if ("Tags" in item):
    tags = item["Tags"]
    for tag in tags:
      if tag in mitsCommon.watchedTags:
        foundTags.append(tag)
  if len(foundTags) == 0:
    foundTags.append(mitsCommon.defaultTag)
  return foundTags

def ignoreSeasonByTag(item):
  if ("Tags" in item):
    tags = item["Tags"]
    for tag in tags:
      if tag == mitsCommon.seasonTagIgnore:
        return True
  return False

def generateSeasons(id, name):
  endpoint = endpointLibraryItems.format(id)
  if excludeLocationTypes != '':
    endpoint += "&excludeLocationTypes=" + excludeLocationTypes
  libraryResponse = requests.get(endpoint, headers=headers)
  libraryData = json.loads(libraryResponse.text)
  seasonItems = libraryData["Items"]
  seasons = []
  folder = mitsCommon.seriesFolders
  for item in seasonItems:
    seasonName = item["Name"]
    if seasonName not in mitsCommon.seasonsToIgnore:
      if (item["LocationType"] not in excludeLocationTypes):
        if startsWithAny(item["Path"], folder):
          season = mitsCommon.Season()
          season.seasonTitle = seasonName
          if "ProductionYear" in item:
            season.year = item["ProductionYear"]

          season.tags = getTags(item)

          if not ignoreSeasonByTag(item):
            seasons.append(season)
  return seasons

def startsWithAny(text, prefixes):
  # checks if the text starts with any of the prefixes in the list.
  return any(text.startswith(prefix) for prefix in prefixes)

def update(fullRefresh):  
  # Send a GET request to the API with headers
  response = requests.get(endpointLibraries, headers=headers)
  # Check for successful response status code
  if response.status_code == 200:
    # Convert JSON response to Python dictionary
    data = json.loads(response.text)

    foundKeys = []
    items = data["Items"]
    for item in items:
      if item["Name"] in Libraries:
        foundKeys.extend (readMediaLibrary(item["Id"], fullRefresh, item["CollectionType"] == "tvshows"))

    if (fullRefresh):  
      mitsData.remove(foundKeys)

  else:
    print(f"API request failed with status code: {response.status_code}")
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

#note: it's bad practice to store api key in code since others can access it
#should resistric use to a certain website url (if this was a web app)
#has been resitricted to only allow use with youtube data api
API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"

#set up api with dev api key
youtube = build('youtube', 'v3', developerKey=API_KEY)

#returns lastest thuumb url based on the imported url (could be username also)
def getThumbnailUrl(channelUrl):
    
    #convert import to id
    channelId = _getChannelId(channelUrl)
    
    #get playlists from user
    playlists = youtube.channels().list(
        id=channelId, 
        part='contentDetails'
    ).execute()

    #if no playlists then must not have uploads or user doesn't exist
    if (len(playlists['items']) == 0):
        thumbnailUrl = None
    else:
        #getting the uploads playlistid
        playlistId = playlists['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        #from playlist with id get first video
        playlistVideos = youtube.playlistItems().list(
            playlistId=playlistId, 
            part="snippet",
            fields="items", 
            maxResults=1
        ).execute()

        #if no videos then must not have videos (possibly private videos)
        if (len(playlistVideos["items"]) == 0):
            thumbnailUrl = None
        else:
            #get url of thumbnail (might throw key error if uploaded thumbnail was low res so just use default)
            try:
                thumbnailUrl = playlistVideos["items"][0]["snippet"]["thumbnails"]["maxres"]["url"]
            except KeyError:
                thumbnailUrl = playlistVideos["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        
    
    return thumbnailUrl


#based on imported url/name get the channel id (if it's a url channel id is just last part)
def _getChannelId(url):
    #split url and get last element
    splitUrl = url.split("/")
    lastElement = splitUrl[len(splitUrl)-1]

    #query ytapi to get channels with that username
    channels = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        forUsername=lastElement,
        maxResults=1
    ).execute()
    
    #if no channels have the username then return the last element (should be id)
    if (len(channels["items"]) == 0):
        return lastElement
    else:
        #returns id corrosponding with username (username is not same as id)
        return channels["items"][0]["id"]



import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup


SPOTIFY_CLIENT_ID = "exampletestexample" #follow guide to get your client ID and secret: https://support.heateor.com/get-spotify-client-id-client-secret/
SPOTIFY_CLIENT_SECRET = "exampletestexample"
spotipy_scope = "playlist-modify-public" #this allows us to add public playlists in your spotify account
SPOTIFY_REDIRECT_URL = "http://localhost:8888/callback" #You should use this for the redirect URL in the spotify dev portal

oauth_dict = SpotifyOAuth(scope = spotipy_scope, client_id= SPOTIFY_CLIENT_ID, client_secret= SPOTIFY_CLIENT_SECRET, redirect_uri = SPOTIFY_REDIRECT_URL, show_dialog= True, cache_path= ".cache") #authentication

sp = spotipy.Spotify(auth_manager= oauth_dict)

URL = "https://www.billboard.com/charts/hot-100/" #top 100 billboard url as a constant

#getting your bithday
user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
#here we get the html file 
response = requests.get(URL + user_date)
web_html = response.text

#
html = BeautifulSoup(web_html, "html.parser")
all_song_names = html.find_all("h3", class_="a-no-trucate")
all_song_names = [songs.getText().strip() for songs in all_song_names]

client = spotipy.client.Spotify(oauth_manager = oauth_dict)





ls = client.current_user_playlists() #gets hold of all playlists the user has
i = 0 
playlist_id = 0
for playlist in ls['items']: #this is to check if the playlist already exists
    if playlist['name'] == user_date + "Top 100":
        playlist_id = playlist['id']
        i = -1

if i == 0: #if it doesnt exit, we create a new playlist
    playlist_id = client.user_playlist_create(sp.current_user()['id'], user_date + "Top 100", public = True)


    song_list = [] 
    for song_name in all_song_names:
        song = client.search(q = song_name + " " + user_date[0:4], limit = 1, offset= 0, type = "track", market= None)
        #this is saying if spotify doesnt have the song we are looking for, we just skip this song entry
        if song['tracks']['total'] == 0: 
            continue
        song_list.append(song['tracks']['items'][0]['uri'])


    client.playlist_add_items(playlist_id, song_list)

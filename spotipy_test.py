import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

scope = "playlist-modify-private playlist-modify-public user-library-modify"
username = "1247468717"
redirect_uri = "http://localhost:8888/callback/"

token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
sp = spotipy.Spotify(auth=token,
                     client_credentials_manager=SpotifyClientCredentials(
                         client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
                     )

# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# # sp.user_playlist_create(username, 'Test SPOTIPY playlist 2')


name = 'chopped in half'
artist = 'obituary'

results = sp.search(q=f'track:{ name} artist:{artist}', type='track', limit=1)
print(json.dumps(results, indent=2))
print(results['tracks']['items'][0]['album']['id'])

#current_user_saved_tracks_add(
sp.current_user_saved_albums_add(['79fVRZLnIqS3FytTLfTBT4'])

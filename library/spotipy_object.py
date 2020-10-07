from dotenv import load_dotenv
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
USERNAME = os.getenv('SPOTIFY_USERNAME')
scope = "playlist-modify-private playlist-modify-public user-library-modify"
redirect_uri = "http://localhost:8888/callback/"

token = util.prompt_for_user_token(USERNAME,
                                   scope,
                                   CLIENT_ID,
                                   CLIENT_SECRET,
                                   redirect_uri
                                   )

spotipy_object = spotipy.Spotify(auth=token,
                                 client_credentials_manager=SpotifyClientCredentials(
                                    client_id=CLIENT_ID, 
                                    client_secret=CLIENT_SECRET
                                    )
                                 )

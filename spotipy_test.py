
import spotipy
import spotipy.util as util
# from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID='4077f916fc784360a6d482594ca43713'
CLIENT_SECRET='de192af6886f453784c692f2791968ae'

scope = "user-library-read"
username = "1247468717"
redirect_uri = "http://localhost:8888/callback/"

token = spotipy.util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
sp = spotipy.Spotify(auth=token)

# token = spotipy.util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# cache_token = token.get_access_token()
# spotify = spotipy.Spotify(cache_token)

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

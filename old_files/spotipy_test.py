from gmusicapi import Mobileclient
import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
import os
import re
from gpm_test import pull_playlists

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

print(sp.user_playlist_create(username, 'Test SPOTIPY playlist 3'))


# name = 'chopped in half'
# artist = 'obituary'

# results = sp.search(q=f'track:{ name} artist:{artist}', type='track', limit=1)
# print(json.dumps(results, indent=2))
# print(results['tracks']['items'][0]['album']['id'])

#current_user_saved_tracks_add(
# sp.current_user_saved_albums_add(['79fVRZLnIqS3FytTLfTBT4'])
'''

FEATURES TO ADD
    - playlist export
        - mass search... might time out
        - create doc of missing files
    - saved album wipe
        - for me only
        - delete every album saved on spotify
    - save all albums from songs I have in library on gpm
        - almost all songs I have are part of saved albums
    - (alternative) save songs as 'liked' on spotify
        - I don't want this but some people might
'''


def import_playlist(playlist_data, username, spotify_object):
    """Import playlist from given playlist object.
    Parameters:
        playlist_data, dictionary with keys:
            name: playlist name as string
            tracks: list of song dictionaries with keys:
                title: song title
                album: album that song is on
                artist: artist of song
        spotify_object: spotipy instance
    Return value: list with values:
        success: boolean value
        missing_tracks:
            list of tracks that were not added to playlist
    """
    name = playlist_data['name']
    tracks = playlist_data['tracks']

    spotify_song_ids = []

    log_file_arr = []
    log_file_arr.append(f'PLAYLIST NAME: {name}')

    for track in tracks:
        track_title = track['title']
        artist = track['artist']
        iters = 0
        while True:
            iters += 1
            track_title = track_title.replace("'", "")
            query = f'track:{track_title} artist:{artist}'
            spotify_results = spotify_object.search(query, type='track', limit=1)
            if len(spotify_results['tracks']['items']) > 0:
                sp_track = spotify_results['tracks']['items'][0]
                if iters > 1:
                    log_file_arr.append(f'\tADDING TRACK: {sp_track["name"]} | {sp_track["album"]["name"]} | {sp_track["artists"][0]["name"]}')
                    log_file_arr.append('\n')
                spotify_song_ids.append(sp_track['id'])
                break
            elif iters == 1:
                pat = r'\s(?:FT\.|FEAT|\().*'
                new_search = re.sub(pat, '', track_title, re.IGNORECASE)
                log_file_arr.append(f'\tNOT FOUND | {artist} | {track_title} | SEARCHING FOR: {new_search}')
                track_title = new_search
            elif iters == 2:
                new_search = track['album_artist']
                log_file_arr.append(f'\tNOT FOUND | {artist} | {track_title} | SEARCHING FOR: {new_search}')
                artist = new_search
            else:
                log_file_arr.append('\n')
                break
    return log_file_arr
    # playlist = spotify_object.user_playlist_create(username, name)
    # spotify_object.user_playlist_add_tracks(user=username, playlist_id=playlist['id'], tracks=spotify_song_ids)


if __name__ == "__main__":

    mc = Mobileclient()
    mc.oauth_login('3b98457227009a89', oauth_credentials='./mobilecredentials.cred')
    playlists = pull_playlists(mc)
    log_file_arr = []
    for playlist in playlists:
        log_file_arr += import_playlist(playlist, username, sp)
    with open('log_file_2.txt', 'w') as f:
        f.write('\n'.join(log_file_arr))

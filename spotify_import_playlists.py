from dotenv import load_dotenv
import json
import os
import re

from gmusicapi import Mobileclient
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from gpm_test import pull_playlists

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

sp = spotipy.Spotify(auth=token,
                     client_credentials_manager=SpotifyClientCredentials(
                        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
                        )
                     )


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
            spotify_results = spotify_object.search(query,
                                                    type='track',
                                                    limit=1
                                                    )

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

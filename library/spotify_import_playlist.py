import re

LOG_FILE = 'log_file_woohoo.txt'


def log_line(line, print_log):
    with open(LOG_FILE, 'a+') as f:
        f.write(line)
        f.write('\n')

    if print_log:
        print(line)


def get_track_id(track, spotify_object, print_log):
    track_title = track['title']
    artist = track['artist']
    iters = 0
    while True:
        iters += 1
        track_title = track_title.replace("'", "")
        artist = artist.replace("'", "")
        query = f'track:{track_title} artist:{artist}'
        spotify_results = spotify_object.search(query,
                                                type='track',
                                                limit=1
                                                )

        if len(spotify_results['tracks']['items']) > 0:
            sp_track = spotify_results['tracks']['items'][0]
            if iters > 1:
                info = f'\tADDING TRACK: {sp_track["name"]} | {sp_track["album"]["name"]} | {sp_track["artists"][0]["name"]}\n'
                log_line(info, print_log)

            return sp_track['id']
            break
        elif iters == 1:
            pat = r'\s(?:FT\.|FEAT|\().*'
            new_search = re.sub(pat, '', track_title, re.IGNORECASE)
            info = f'\tNOT FOUND | {artist} | {track_title} | SEARCHING FOR: {new_search}'
            log_line(info, print_log)
            track_title = new_search
        elif iters == 2:
            new_search = track['album_artist']
            info = f'\tNOT FOUND | {artist} | {track_title} | SEARCHING FOR: {new_search}'
            log_line(info, print_log)
            artist = new_search
        else:
            log_line('\n', print_log)
            return False


def import_playlist(playlist_data, username, spotify_object, print_log=True):
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

    log_line(f'PLAYLIST NAME: {name}', print_log)

    for track in tracks:
        id = get_track_id(track, spotify_object, print_log)
        if id:
            spotify_song_ids += id

    # return log_file_arr
    # playlist = spotify_object.user_playlist_create(username, name)
    # spotify_object.user_playlist_add_tracks(user=username, playlist_id=playlist['id'], tracks=spotify_song_ids)

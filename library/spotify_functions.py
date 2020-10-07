import re

PLAYLIST_LOG_FILE = 'playlist_import.log'
ALBUM_LOG_FILE = 'album_import.log'


def log_line(line, print_log, filename):
    with open(filename, 'a+') as f:
        f.write(line)
        f.write('\n')

    if print_log:
        print(line)


def get_track_id(track, spotify_object, print_log):
    track_title = track['title']
    artist = track['artist']
    iters = 0
    info_arr = []
    while True:
        iters += 1
        track_title = track_title.replace("'", "")
        artist = artist.replace("'", "")
        query = f'track:{track_title} artist:{artist}'
        spotify_results = spotify_object.search(query,
                                                type='track',
                                                limit=1)

        if len(spotify_results['tracks']['items']) > 0:
            sp_track = spotify_results['tracks']['items'][0]
            if iters > 1:
                info_arr.append(f'\tADDING TRACK: {sp_track["name"]} | {sp_track["album"]["name"]} | {sp_track["artists"][0]["name"]}\n')

            return sp_track['id']
            break
        elif iters == 1:
            pat = r'\s(?:FT\.|FEAT|\().*'
            new_search = re.sub(pat, '', track_title, re.IGNORECASE)
            info_arr.append(f'\tNOT FOUND | {artist} | {track_title} | SEARCHING FOR: {new_search}')
            track_title = new_search
        elif iters == 2:
            new_search = track['album_artist']
            info_arr.append(f'\tNOT FOUND | {artist} | {track_title} | SEARCHING FOR: {new_search}')
            artist = new_search
        else:
            log_line('\n'.join(info_arr), print_log, PLAYLIST_LOG_FILE)
            return False


def get_album_ids(album_data, spotify_object):
    album_ids = []
    for album in album_data:
        album_name = album['name'].replace("'", "")
        artist = album['artist'].replace("'", "")
        query = f'album:{album_name} artist:{artist}'
        search_results = spotify_object.search(query,
                                               type='album',
                                               limit=1)
        if search_results['albums']['items']:
            album_ids.append(search_results['albums']['items'][0]['id'])
        else:
            log_line(f'Album not found: {album_name} by {artist}', True, ALBUM_LOG_FILE)
    return album_ids


def save_albums(album_ids, spotify_object):
    spotify_object.current_user_saved_albums_add(album_ids)


def get_all_saved_album_ids(username, spotify_object):
    """Return list of album ids for all saved albums for given username."""
    album_ids = []
    offset = 0
    limit = 50
    while True:
        results = spotify_object.current_user_saved_albums(
            limit=50, offset=offset)
        for album in results['items']:
            album_ids.append(album['album']['id'])
        if results['next']:
            offset += limit
        else:
            break
    return album_ids


def remove_all_saved_albums(spotify_object):
    album_ids = get_all_saved_album_ids(spotify_object)
    spotify_object.current_user_saved_albums_delete(album_ids)


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

    log_line(f'PLAYLIST NAME: {name}', print_log, PLAYLIST_LOG_FILE)

    for track in tracks:
        id = get_track_id(track, spotify_object, print_log)
        if id:
            spotify_song_ids += [id]
    playlist = spotify_object.user_playlist_create(username, name)
    offset = 0
    size = 50
    while True:
        start = offset
        end = start + size
        playlist_chunk = spotify_song_ids[start:end]
        spotify_object.user_playlist_add_tracks(
            user=username, playlist_id=playlist['id'], tracks=playlist_chunk)
        if len(playlist_chunk) < size:
            break
        else:
            offset += size


if __name__ == "__main__":
    import sys
    [sys.path.append(i) for i in ['.', '..']]

    from library.spotipy_object import USERNAME, spotipy_object as sp

    print(get_all_saved_album_ids(USERNAME, sp))

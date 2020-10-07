def pull_playlists(mobile_client):
    playlists_arr = []
    gpm_playlists = mobile_client.get_all_user_playlist_contents()
    for gpm_playlist in gpm_playlists:
        playlist = {'tracks': []}
        playlist['name'] = gpm_playlist['name']
        for track in gpm_playlist['tracks']:
            if track['source'] == '2':
                song = {
                    'title': track['track']['title'],
                    'album': track['track']['album'],
                    'artist': track['track']['artist'],
                    'album_artist': track['track']['albumArtist']
                }
                playlist['tracks'].append(song)
        playlists_arr.append(playlist)
    return playlists_arr


def pull_liked_songs(mobile_client):
    """Return dictionary with values:
        name: 'gpm_liked_songs'; Hard-coded
        tracks: list of song dictionaries with keys:
            title: song title
            album: album that song is on
            artist: artist of song
        Emulates playlist_data format used in spotipy_import_playlist
    """
    gpm_songs = mobile_client.get_top_songs()
    songs_arr = []
    for gpm_song in gpm_songs:
        song = {
            'title': gpm_song['title'],
            'album': gpm_song['album'],
            'artist': gpm_song['artist'],
            'album_artist': gpm_song['albumArtist']
        }
        songs_arr.append(song)

    return {
        'name': 'gpm_liked_songs',
        'tracks': songs_arr
    }


def pull_saved_songs(mobile_client):
    gpm_songs = mobile_client.get_all_songs()
    songs_arr = []
    for gpm_song in gpm_songs:
        song = {
            'title': gpm_song['title'],
            'album': gpm_song['album'],
            'artist': gpm_song['artist'],
            'album_artist': gpm_song['albumArtist']
        }
        songs_arr.append(song)
    return songs_arr


if __name__ == "__main__":
    import sys
    [sys.path.append(i) for i in ['.', '..']]
    from library.gpm_mobileclient import gpm_mobileclient as mc

    songs = pull_liked_songs(mc)
    print(songs)

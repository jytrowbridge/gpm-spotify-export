import sys
[sys.path.append(i) for i in ['.', '..']]

from library.gpm_mobileclient import gpm_mobileclient as mc
from library.spotipy_object import USERNAME, spotipy_object as sp
from library.gpm_functions import pull_playlists, pull_liked_songs
from library.spotify_functions import import_playlist, get_all_playlists


def import_all_playlists():
    """Import all playlists from gpm into spotify.
    Returns True if successful, False otherwise.
    """

    print("Pulling all playlists from GPM...")
    gpm_playlists = pull_playlists(mc)
    print("Pulling liked songs as playlist from GPM...")
    liked_songs_playlist = pull_liked_songs(mc)
    all_playlists = gpm_playlists + [liked_songs_playlist] 

    print("Importing playlists into spotify...")
    extant_playlists = get_all_playlists(sp)
    for playlist in all_playlists:
        if playlist['tracks'] and playlist['name'] not in extant_playlists:
            import_playlist(playlist, USERNAME, sp)


if __name__ == "__main__":
    import_all_playlists()

import sys
[sys.path.append(i) for i in ['.', '..']]

from library.gpm_mobileclient import gpm_mobileclient as mc
from library.spotipy_object import USERNAME, spotipy_object as sp
from library.gpm_functions import pull_playlists, pull_liked_songs, pull_saved_songs
from library.spotify_import_playlist import import_playlist


def import_all_playlists():
    """Import all playlists from gpm into spotify.
    Returns True if successful, False otherwise.
    """

    print("Pulling all playlists from GPM...")
    # gpm_playlists = pull_playlists(mc)
    print("Pulling liked songs as playlist from GPM...")
    liked_songs_playlist = pull_liked_songs(mc)
    # all_playlists = gpm_playlists + [liked_songs_playlist] 
    all_playlists = [liked_songs_playlist] 

    print("Importing playlists into spotify...")
    # master_log = []
    for playlist in all_playlists:
        # master_log += import_playlist(playlist, USERNAME, sp)
        import_playlist(playlist, USERNAME, sp)

    # with open('log_file.txt', 'w') as f:
        # f.write('\n'.join(master_log))


if __name__ == "__main__":
    import_all_playlists()

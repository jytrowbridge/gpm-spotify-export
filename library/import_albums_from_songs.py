import sys
[sys.path.append(i) for i in ['.', '..']]
from library.gpm_functions import pull_saved_albums_thru_songs
from library.spotify_functions import get_album_ids, save_albums
from library.spotipy_object import USERNAME, spotipy_object as sp
from library.gpm_mobileclient import gpm_mobileclient as mc


def import_albums_from_songs():
    gpm_albums = pull_saved_albums_thru_songs(mc)
    album_ids = get_album_ids(gpm_albums, sp)
    save_albums(album_ids, sp)


if __name__ == "__main__":
    import_albums_from_songs()

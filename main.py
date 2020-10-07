import argparse
from library.export_playlists import import_all_playlists
from library.import_albums_from_songs import import_albums_from_songs
from library.spotify_functions import remove_all_saved_albums
from library.spotipy_object import USERNAME, spotipy_object as sp


def main():
    parser = argparse.ArgumentParser(
        description='Import music from GPM account into Spotify.'
        )

    parser.add_argument('--rem-spotify-albums',
                        action='store_true',
                        help='Include to remove all saved albums for \
                                configured spotify user.')

    parser.add_argument('--import-playlists',
                        action='store_true',
                        help='Include to import all playlists into spotify.\
                            Liked songs are imported as a playlist.')

    parser.add_argument('--import-saved-song-albums',
                        action='store_true',
                        help='Include to save albums on spotify matching every \
                            saved song in google play music. GPM API doesn\'t \
                            have method for returning saved albums.')

    args = parser.parse_args()

    if args.rem_spotify_albums:
        if args.import_playlists or args.import_saved_song_albums:
            print("Only one flag may be set at a time")
            return False
        print('Attempting to remove all saved albums for configured user...')
        remove_all_saved_albums(sp)

    elif args.import_playlists:
        if args.rem_spotify_albums or args.import_saved_song_albums:
            print("Only one flag may be set at a time")
            return False
        print('Attempting to import playlists...')
        import_all_playlists()

    elif args.import_saved_song_albums:
        if args.rem_spotify_albums or args.import_playlists:
            print("Only one flag may be set at a time")
            return False
        print("Attempting to import saved song albums...")
        import_albums_from_songs()

    else:
        print("noooo")


if __name__ == "__main__":
    main()

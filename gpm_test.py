from gmusicapi import Mobileclient

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
                    'artist': track['track']['albumArtist']
                }
            playlist['tracks'].append(song)
        playlists_arr.append(playlist)
    return playlists_arr


def pull_saved_songs(mobile_client):
    gpm_songs = mobile_client.get_all_songs()
    songs_arr = []
    for gpm_song in gpm_songs:
        song = {
            'title': gpm_song['title'],
            'album': gpm_song['album'],
            'artist': gpm_song['artist']
        }
        songs_arr.append(song)
    return songs_arr


if __name__ == "__main__":

    mc = Mobileclient()
    # oauth_creds = mc.perform_oauth('./mobilecredentials.cred')
    # oauth_creds = mc.perform_oauth(open_browser=True)

    mc.oauth_login('3b98457227009a89', oauth_credentials='./mobilecredentials.cred')
    # mc.oauth_login(mc.FROM_MAC_ADDRESS, oauth_credentials=oauth_creds)

    # print(pull_playlists(mc))

    print(len(pull_saved_songs(mc)))
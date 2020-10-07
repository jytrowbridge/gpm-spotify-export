from gmusicapi import Mobileclient
from os import path


credentials_filename = 'mobilecredentials.cred'
gpm_mobileclient = Mobileclient()

oauth_creds = credentials_filename if path.exists(credentials_filename) else \
              gpm_mobileclient.perform_oauth('./mobilecredentials.cred',
                                             open_browser=True)

gpm_mobileclient.oauth_login('3b98457227009a89', oauth_credentials=oauth_creds)

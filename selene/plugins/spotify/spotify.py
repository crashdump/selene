import os
import sys

try:
    SPOTIPY_CLIENT_ID = os.environ['SPOTIFY_ID']
    SPOTIPY_CLIENT_SECRET = os.environ['SPOTIFY_SECRET']
except KeyError:
    print('Please define the environment variables SPOTIFY_ID and SPOTIFY_SECRET')
    sys.exit(1)

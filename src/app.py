import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt



load_dotenv()


client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

Artist_Id = "1qto4hHid1P71emI6Fd8xi"
Artist_Name ="Aventura"

results = sp.search(q='artist:' + Artist_Name, type='artist')
artist = results['artists']['items'][0]
artist_id = artist['id']

# Las canciones más populares del artista
top_tracks = sp.artist_top_tracks(Artist_Id)

#Top 10 de canciones
for idx, track in enumerate(top_tracks['tracks'][:10]):
    print(f"{idx + 1}. {track['name']}")

def get_all_tracks(artist_id):
    all_tracks = []
    results = sp.artist_top_tracks(artist_id)
    all_tracks.extend(results['tracks'])
    return all_tracks
# Obtén todos los tracks del artista
all_tracks = get_all_tracks(artist_id)
# Crea un DataFrame con los tracks
tracks_data = {
    "name": [track['name'] for track in all_tracks],
    "album": [track['album']['name'] for track in all_tracks],
    "release_date": [track['album']['release_date'] for track in all_tracks],
    "popularity": [track['popularity'] for track in all_tracks],
    "duration_ms": [track['duration_ms'] for track in all_tracks]
}


df = pd.DataFrame(tracks_data)
df['duration_min'] = df['duration_ms'] / 60000


plt.figure(figsize=(10, 6))
plt.scatter(df['release_date'], df['popularity'], alpha=0.6)
plt.title('Popularidad de las canciones de Aventura a lo largo del tiempo')
plt.xlabel('Fecha de lanzamiento')
plt.ylabel('Popularidad')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()



plt.figure(figsize=(10, 6))
plt.scatter(df['duration_min'], df['popularity'], alpha=0.6)
plt.title('Popularidad de las canciones de Aventura en función de la duración')
plt.xlabel('Duración (minutos)')
plt.ylabel('Popularidad')
plt.grid(True)
plt.show()


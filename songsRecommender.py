import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib
import os
from random import choice
# Load the song data from CSV
song_data = pd.read_csv('songdata2.csv')

# Load the model from disk if it exists, otherwise train the model and save it to disk
if os.path.exists('knn_model.pkl') and os.path.exists('vectorizer.pkl'):
    knn_model = joblib.load('knn_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    print("Loaded model and vectorizer from disk")
else:
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(song_data['text'])
    knn_model = NearestNeighbors(n_neighbors=5, algorithm='brute', metric='cosine')
    knn_model.fit(tfidf_matrix)
    joblib.dump(knn_model, 'knn_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("Saved model and vectorizer to disk")

def recommend_songs(input_song):
    input_song = input_song.lower()
    if input_song not in song_data['song'].values:
        return "Input song does not exist in the dataset."
    
    input_song_tfidf = vectorizer.transform([input_song])
    distances, indices = knn_model.kneighbors(input_song_tfidf)
    recommended_songs = song_data.iloc[indices[0]]
    
    recommended_songs_list = recommended_songs[['song', 'artist']].apply(lambda x: ' - '.join(x), axis=1).tolist()
    
    return choice(recommended_songs_list)

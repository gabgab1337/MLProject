from flask import Flask, request, jsonify
import requests
import base64
import songsRecommender

app = Flask(__name__)

@app.route('/spotify-token', methods=['GET'])
def spotify_token():
    clientId = '2110b23bb83c4f6cb18f91ecb74faced'
    clientSecret = '9bc14d46bc6e4fd7ad8462990dbaebe5'
    auth = base64.b64encode(f'{clientId}:{clientSecret}'.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return jsonify(response.json())

@app.route('/recommend', methods=['POST'])
def recommend():
    song = request.json['song']
    recommendations = songsRecommender.recommend_songs(song)
    return jsonify(recommendations)

@app.route('/')
def home():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(port=5500)
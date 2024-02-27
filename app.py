from flask import Flask, render_template
import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context #Para evitar errores de certificado SSL

app = Flask(__name__)

@app.route('/')
def get_list_elements_page():
    url = "https://rickandmortyapi.com/api/character/"
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    data = response.read()
    dict = json.loads(data)
    
    return render_template("characters.html", characters=dict['results'])

@app.route('/profile/<id>')
def get_profile(id):
    url = "https://rickandmortyapi.com/api/character/"+id #+id
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    data = response.read()
    dict = json.loads(data)
    
    return render_template("profile.html", profile=dict)

@app.route('/lista')
def get_list_elements():
    url = "https://rickandmortyapi.com/api/character/"
    context = ssl._create_unverified_context()

    try:
        response = urllib.request.urlopen(url, context=context)
        characters = response.read()
        dict = json.loads(characters)

        characters_list = []

        for character in dict['results']:
            character_data = {
                "name": character['name'],
                "status": character['status'],
                "species": character['species'],
            }
            characters_list.append(character_data)
        
        return {"characters": characters_list}
    except Exception as e:
        return {"error": str(e)}
    
@app.route('/locations')
def get_locations():
    url = "https://rickandmortyapi.com/api/location"
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    locations_data = json.loads(data)
    locations = locations_data['results']
    return render_template("locations.html", locations=locations)

@app.route('/location/<id>')
def get_location(id):
    url = "https://rickandmortyapi.com/api/location/"+id
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    data = response.read()
    location_dict = json.loads(data)

    
    characters_data = []
    for resident_url in location_dict['residents']:
        with urllib.request.urlopen(resident_url, context=context) as response:
            character_data = json.loads(response.read())
            characters_data.append(character_data)

    return render_template("location.html", location=location_dict, characters=characters_data)

@app.route('/episodes')
def get_episodes():
    url = "https://rickandmortyapi.com/api/episode"
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    episodes_data = json.loads(data)
    episodes = episodes_data['results']
    return render_template("episodes.html", episodes=episodes)

@app.route('/episode/<id>')
def get_episode(id):
    url = "https://rickandmortyapi.com/api/episode/"+id
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    data = response.read()
    episode_dict = json.loads(data)

    characters_data = []
    for character_url in episode_dict['characters']:
        with urllib.request.urlopen(character_url, context=context) as response:
            character_data = json.loads(response.read())
            characters_data.append(character_data)

    return render_template("episode.html", episode=episode_dict, characters=characters_data)

if __name__ == '__main__':
    app.run(debug=True)

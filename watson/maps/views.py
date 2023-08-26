from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv, find_dotenv
import os
import folium
from api_utils import courses
import pickle

def index(request):
    api_url = get_url()
    current_courses = courses.get_current_courses(api_url, debug=True)
    # for course, info in current_courses.items():
        # current_courses info['location']

    # create map centered on UQ
    m = folium.Map(location=[-27.49894, 153.01368], zoom_start=19)

    # add building coords
    buildings = load_buildings()
    for ref, tags in buildings.items():
        coords = (tags['lat'], tags['lon'])
        folium.Marker(coords).add_to(m)
    
    # create context for page
    context = {
        'map': m._repr_html_()
        }

    return render (request, "index.html", context)

def get_url() -> str:
    load_dotenv(find_dotenv())
    return os.environ["API_URL"]

def load_buildings() -> dict:
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'data/buildings.pickle')
    with open(file_path, 'rb') as handle:
        data = pickle.load(handle)
    return data
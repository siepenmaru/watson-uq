from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv, find_dotenv
import os
import folium
from api_utils import courses
from .forms import TimeForm
from datetime import datetime
import pickle

def index(request):
    api_url = get_url()
    if request.method == "POST":
        print(request.POST)
        form = TimeForm(request.POST)
        if form.is_valid():
            # try:
            idx = form.cleaned_data['date_index']
            time: datetime = form.cleaned_data['selected_time']
            current_courses = courses.get_current_courses(api_url, idx, time, False, debug=False)
            # except:
            #     # FIXME: debug mode
            #     current_courses = courses.get_current_courses(api_url, 1, "10:00", False, debug=True)
        else:
            # FIXME: debug mode
            current_courses = courses.get_current_courses(api_url, 1, "10:00", False, debug=True)
    else:
        current_courses = courses.get_current_courses(api_url, 1, "10:00", True, debug=True)


    # create map centered on UQ
    m = folium.Map(location=[-27.49894, 153.01368], zoom_start=19, max_zoom=19)


    # add building coords
    buildings = load_buildings()

    info: dict
    for course, info in current_courses.items():
        # FIXME: What if there are multiple lectures going on in the same building????
        try:
            building = buildings[info["building_id"]]
            coords = (building['lat'], building['lon'])
            
            icon = 'graduation-cap'
            match info['faculty']:
                case 'EAIT': icon = 'desktop'
                case 'BEL': icon = 'arrow-trend-up'
                case 'HLBS': icon = 'people-group'
                case 'HSS': icon = 'earth-asia'
                case 'SCI': icon = 'flask'
                case 'MED': icon = 'staff-snake'
                case default: pass

            label = folium.Html(
                f"""
                <h2>{course}</h2>
                <p style="font-size:150%">{info['desc']}</p>
                <ul style="font-size:120%">
                    <li>Faculty: {info['faculty']}</li>
                    <li>Building: {info['building_id']} - {info['building_name']}</li>
                    <li>Room: {info['room_id']}</li>
                    <li>Start time: {info['start_time']}</li>
                    <li>Duration: {info['duration']} minutes</li>
                </ul>
                """, script=True
            )

            folium.Marker(
                coords, icon=folium.Icon(color='purple', icon=icon, prefix='fa')).add_child(
                    folium.Popup(label, parse_html=True, max_width=300)).add_to(m)
        except:
            # idc
            continue
        # current_courses = info['location']

    # for ref, tags in buildings.items():
    #     coords = (tags['lat'], tags['lon'])
    #     folium.Marker(coords).add_to(m)
    
    # create context for page
    context = {
        'map': m._repr_html_(),
        'time_form': form
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
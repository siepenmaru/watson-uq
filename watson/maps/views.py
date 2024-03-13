from django.shortcuts import render
from dotenv import load_dotenv, find_dotenv
import os
import folium
from folium.plugins import MarkerCluster
import branca
from api_utils import courses
from .forms import TimeForm
from datetime import datetime
from zoneinfo import ZoneInfo
from api_utils.misc import floor_hour
from api_utils.geo import get_user_loc
import pickle
from branca.element import Template, MacroElement

def index(request):
    # TODO: handle multiple lecs in one building
    api_url = get_url()
    if request.method == "POST":
        print(request.POST)
        form = TimeForm(request.POST)
        if form.is_valid():
            idx = form.cleaned_data['date_index']
            time: datetime = form.cleaned_data['selected_time']
            current_courses = courses.get_current_courses(api_url, idx, time, False, debug=False)
        else:
            # FIXME: debug mode
            current_courses = courses.get_current_courses(api_url, 1, "10:00", False, debug=True)
    else:
        dt = datetime.now(ZoneInfo("Australia/Brisbane"))
        form = TimeForm(
            initial={
                'date_index': dt.date().strftime('%w'),
                'selected_time': floor_hour(dt).replace(minute=0).time()
            }
        )
        
        current_courses = courses.get_current_courses(api_url, 1, dt, True, debug=False)


    # create map centered on UQ
    fig = branca.element.Figure(height="100%")
    m = folium.Map(location=[-27.49894, 153.01368], zoom_start=19, max_zoom=19)
    cluster = MarkerCluster(options={
        "animate": True,
        "spiderfyDistanceMultiplier": 2
    }).add_to(m)
    template = get_template()
    macro = MacroElement()
    macro._template = Template(template)

    # m.get_root().add_child(macro)
    fig.add_child(m)
    fig.add_child(macro)
    
    # get user location
    user_loc = get_user_loc(cheat_mode=True)

    # add building coords
    buildings = load_buildings()

    info: dict
    for course, info in current_courses.items():
        # FIXME: What if there are multiple lectures going on in the same building????
        try:
            building = buildings[info["building_id"]]
            # if building not in visited:
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
                <h2>{course} | {info['building_id']}-{info['room_id']}</h2>
                <p style="font-size:200%; margin-top:0.25em; margin-bottom:0.25em;">{info['desc']}</p>
                <ul style="font-size:150%">
                    <li><b>Building name:</b> {info['building_name']}</li>
                    <li><b>Start time:</b> {info['start_time']}</li>
                    <li><b>Duration:</b> {info['duration']} minutes</li>
                </ul>
                <div class='text-center'>
                <button style="height:36px; width:184px;">
                    <a 
                        href="https://my.uq.edu.au/programs-courses/course.html?course_code={course}" target="_blank" rel="noopener noreferrer"
                            style="font-size:1.875em;"
                        >
                    Course Page
                    </a>
                </button>
                <button style="height:36px; width:184px;">
                    <a 
                        href="https://www.openstreetmap.org/directions?engine=fossgis_osrm_foot&route={user_loc[0]}%2C{user_loc[1]}%3B{coords[0]}%2C{coords[1]}" target="_blank" rel="noopener noreferrer"
                            style="font-size:1.875em;"
                        >
                    Navigate Here!
                    </a>
                </button>
                </div>
                """, script=True
            )

            folium.Marker(
                coords, icon=folium.Icon(color='purple', icon=icon, prefix='fa')).add_child(
                    folium.Popup(label, parse_html=True, max_width=300)).add_to(cluster)
        except:
            # idc
            continue
        # current_courses = info['location']

    # for ref, tags in buildings.items():
    #     coords = (tags['lat'], tags['lon'])
    #     folium.Marker(coords).add_to(m)
    
    # create context for page
    context = {
        # 'map': m._repr_html_(),
        'map': fig._repr_html_(),
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

def get_template() -> str:
    # FIXME: why have I done this
    # https://nbviewer.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd
    return """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; top: 20px;'>
     
<div class='legend-title' style="font-size:1em;">
    <strong>Faculties</strong>
</div>
<div class='legend-scale'>
  <ul class='legend-labels' style="font-size:1em; text-align: left">
    <li>
        <b><i class="fa-solid fa-desktop"></i></b>
            : EAIT</li>
    <li>
        <b><i class="fa-solid fa-arrow-trend-up"></i></b>
            : BEL</li>
    <li>
        <b><i class="fa-solid fa-people-group"></i></b>
            : HABS</li>
    <li>
        <b><i class="fa-solid fa-earth-asia"></i></b>
            : HASS</li>
    <li>
        <b><i class="fa-solid fa-flask"></i></b>
            : SCI</li>
    <li>
        <b><i class="fa-solid fa-staff-snake"></i></b>
            : MED</li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
  .alignMe b {
    display: inline-block;
    width: 50%;
    position: relative;
    padding-right: 10px
  }
  .alignMe b::after {
    content: ":";
    position: absolute;
    right: 10px;
  }
</style>
{% endmacro %}"""

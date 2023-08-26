import requests
from datetime import datetime, timedelta
import overpy
from .misc import floor_hour, ceil_hour

def get_course(
        url, search_term, semester, faculty, activity_type, days, start_time, end_time
        ) -> requests.Response:
    day_str = ""
    for day in days:
        day_str += f"&day={day}"

    body = f"search-term={search_term}&semester={semester}&campus=STLUC&faculty={faculty}&type={activity_type}{day_str}&start-time={start_time}&end-time={end_time}"

    response = requests.post(url, body)

    return response

def get_current_courses(url, debug=False) -> dict:
    # slow as all hell. fix???
    faculties = ["EAIT", "BEL", "HLBS", "HSS", "SCI", "MED"]

    if debug:
        days = [1] # monday
        start_time = "10:00"
        end_time = "11:00"
    else:
        dt = datetime.now()
        days = [dt.date().strftime('%w')]
        start_time = floor_hour(dt).strftime("%H:%M")
        end = ceil_hour(dt).strftime("%H:%M")

    courses: dict = {}
    for faculty in faculties:
        json_dict: dict = get_course(url, "", "S2", faculty, "Lecture", days, start_time, end_time).json()
        for _, v in json_dict.items():
            try:
                activity = next(iter(v['activities'].values()))

                if activity['campus'] == 'ONLINE':
                    continue
                
                loc_info = parse_location(activity['location'])

                courses[v["callista_code"]] = {
                    "desc": v['description'],
                    'start_time': activity['start_time'],
                    'duration': activity['duration'],
                    'building_id': loc_info['building_id'], 
                    'room_id': loc_info['room_id'],
                    'building_name': loc_info['building_name']
                    }
            except Exception:
                # ¯\_(ツ)_/¯
                continue

    return courses

def parse_location(loc: str) -> dict:
    substrs = [substr.strip() for substr in loc.split('-')]
    loc_info = {
        "building_id" : substrs[0],
        "room_id" : substrs[1],
        "building_name" : substrs[2::]
    }
    return loc_info
import requests

def get_course(url, search_term, semester, faculty, activity_type, days, start_time, end_time):
    day_str = ""
    for day in days:
        day_str += f"&day={day}"

    body = f"search-term={search_term}&semester={semester}&campus=STLUC&faculty={faculty}&type={activity_type}{day_str}&start-time={start_time}&end-time={end_time}"

    response = requests.post(url, body)

    return response
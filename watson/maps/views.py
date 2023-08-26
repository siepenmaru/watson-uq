from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv, find_dotenv
import os
import folium

def index(request):
    # centered on UQ
    m = folium.Map(location=[-27.49894, 153.01368], zoom_start=19)
    context = {
        'map': m._repr_html_()
        }
    return render (request, "index.html", context)

def get_url() -> str:
    load_dotenv(find_dotenv())
    return os.environ["API_URL"]
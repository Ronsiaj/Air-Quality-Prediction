import json
import pandas as pd
import numpy as np
import shutil
import urllib.parse
from urllib.request import urlopen


responsetext="http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=10.862088&lon=78.698415&appid=fe53b529190bb5029caf9b5e299d8503"

with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=10.862088&lon=78.698415&appid=fe53b529190bb5029caf9b5e299d8503") as url:
    data = json.load(url)
    #print(data)
    json_object = json.dumps(data, indent=4)
     
    # Writing to sample.json
    with open("static/airdata.json", "w") as outfile:
        outfile.write(json_object)

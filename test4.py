import json
import pandas as pd
import numpy as np
import shutil
import urllib.parse
from urllib.request import urlopen


f = open('static/airdata.json')
 
# returns JSON object as 
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
j=0
for i in data['list']:
    if j<2:
        #print(i)
        data1=i
        #print(data1['components'])
        d1=data1['components']
        print(d1['no'])
        
    j+=1
    

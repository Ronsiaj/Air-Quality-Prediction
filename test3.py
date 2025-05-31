# import the necessary libraries
import numpy as np 
import pandas as pd 
import os

# Visualisation libraries
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
sns.set()
import pycountry
from plotly.subplots import make_subplots

import plotly.express as px
from plotly.offline import init_notebook_mode, iplot 
import plotly.graph_objs as go
import plotly.offline as py
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
#!pip install chart_studio
import chart_studio.plotly as py
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff

import cufflinks
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='pearl')
#py.init_notebook_mode(connected=True)
# color pallette
cnf, dth, rec, act,wth,sth = '#393e46', '#ff2e63', '#21bf73', '#fe9801','#456fe3','#78ffee' 
#Geographical Plotting
import folium
from folium import Choropleth, Circle, Marker
from folium import plugins
from folium.plugins import HeatMap, MarkerCluster
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters() 

from plotly.offline import plot, iplot, init_notebook_mode
init_notebook_mode(connected=True)
#Racing Bar Chart
#!pip install bar_chart_race
import bar_chart_race as bcr
from IPython.display import display_html
# Increase the default plot size and set the color scheme
plt.rcParams['figure.figsize'] = 8, 5
plt.style.use("fivethirtyeight")# for pretty graphs


# Disable warnings 
import warnings
warnings.filterwarnings('ignore')

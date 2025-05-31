from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from math import pi
import json
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import mysql.connector

# Visualisation libraries
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import pycountry
from plotly.subplots import make_subplots

import plotly.express as px
from plotly.offline import init_notebook_mode, iplot 
import plotly.graph_objs as go
import plotly.offline as py
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import chart_studio.plotly as py

import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
#from IPython.display import display_html
#import cufflinks
#cufflinks.go_offline()
#cufflinks.set_config_file(world_readable=True, theme='pearl')
#py.init_notebook_mode(connected=True)
# color pallette
cnf, dth, rec, act,wth,sth = '#393e46', '#ff2e63', '#21bf73', '#fe9801','#456fe3','#78ffee' 
#Geographical Plotting
#import folium
#from folium import Choropleth, Circle, Marker
#from folium import plugins
#from folium.plugins import HeatMap, MarkerCluster
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters() 

#from plotly.offline import plot, iplot, init_notebook_mode
#init_notebook_mode(connected=True)
#Racing Bar Chart
#import bar_chart_race as bcr
#from IPython.display import display_html
# Increase the default plot size and set the color scheme
#plt.rcParams['figure.figsize'] = 8, 5
#plt.style.use("fivethirtyeight")# for pretty graphs


#from IPython.core.display import display_html
##
import glob
#from keras.models import Sequential, load_model
#import keras as k
#from keras.layers import Dense
#from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
#from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
#from tensorflow.keras.optimizers import Adam
##
# Disable warnings 
#import warnings
#warnings.filterwarnings('ignore')


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="air_quality"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    act=request.args.get('act')
    
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cu_owner where uname=%s && pass=%s && status=1",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            result=" Your Logged in sucessfully**"
            return redirect(url_for('owner_home')) 
        else:
            msg="Invalid Username or Password!"
            result="Your logged in fail!!!"
        

    return render_template('index.html',msg=msg,act=act)

@app.route('/login',methods=['POST','GET'])
def login():
    cnt=0
    act=""
    msg=""
    mycursor = mydb.cursor()
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        
        mycursor.execute("SELECT count(*) FROM ar_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            msg="Invalid Username or Password!"
        

    return render_template('login.html',msg=msg,act=act)

@app.route('/login1',methods=['POST','GET'])
def login1():
    cnt=0
    act=""
    msg=""
    mycursor = mydb.cursor()
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        
        mycursor.execute("SELECT count(*) FROM air_user where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('map1')) 
        else:
            msg="Invalid Username or Password!"
        

    return render_template('login1.html',msg=msg,act=act)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
   
    mycursor = mydb.cursor()
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    
    if request.method=='POST':
        name=request.form['name']
       
        mobile=request.form['mobile']
        email=request.form['email']
      
        uname=request.form['uname']
        pass1=request.form['pass']
       
        mycursor.execute('SELECT count(*) FROM air_user WHERE uname = %s', (uname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM air_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
    
            sql = "INSERT INTO air_user(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,uname,pass1)
            mycursor.execute(sql, val)
            mydb.commit()            
            
            msg="success"
 
        else:
            msg='fail'
            
    return render_template('register.html',msg=msg)


@app.route('/login_user',methods=['POST','GET'])
def login_user():
    cnt=0
    act=""
    msg=""
    rdat=[]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM air_geo_location where id>1")
    ds = mycursor.fetchall()

    for dw in ds:
        d1=dw[2].split("new google.maps.LatLng(")
        
        d2=d1[1].split('),')
        #print(d2[0])
        dt=[]
        dt.append(d2[0])
        dt.append(dw[1])
        rdat.append(dt)
        
        
    
    if request.method == 'POST':
        location = request.form['location']

        loc=location.split(",")
        lat=loc[0]
        lon=loc[1]
        
        responsetext="http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=10.862088&lon=78.698415&appid=fe53b529190bb5029caf9b5e299d8503"

        with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat="+lat+"&lon="+lon+"&appid=fe53b529190bb5029caf9b5e299d8503") as url:
            data = json.load(url)
            #print(data)
            json_object = json.dumps(data, indent=4)
             
            # Writing to sample.json
            with open("static/airdata.json", "w") as outfile:
                outfile.write(json_object)
        #####
        
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
                c1=data1['components']
                v1=c1['co']
                v2=c1['no']
                v3=c1['no2']
                v4=c1['o3']
                v5=c1['so2']
                v6=c1['pm2_5']
                v7=c1['pm10']
                v8=c1['nh3']
                air=str(v1)+","+str(v2)+","+str(v3)+","+str(v4)+","+str(v5)+","+str(v6)+","+str(v7)+","+str(v8)
                ff=open("static/air.txt","w")
                ff.write(air)
                ff.close()
                
            j+=1
        msg="ok"    

        
        

    return render_template('login_user.html',msg=msg,act=act,rdat=rdat)


@app.route('/map1', methods=['GET', 'POST'])
def map1():
    msg=""
    aid=""
    view=[]
    result=[]
    img=""
    name=""
    mess=""
    mobile=""
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM air_user where uname=%s",(uname,))
    usr = mycursor.fetchone()
    name=usr[1]
    mobile=str(usr[2])
    
    if request.method=='POST':
        detail=request.form['detail']
        #location=request.form['location']
        
        '''mycursor.execute("SELECT max(id)+1 FROM air_geo_location")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        
        sql = "INSERT INTO air_geo_location(id,location,detail) VALUES (%s, %s, %s)"
        val = (maxid,location,detail)
        act="success"
        mycursor.execute(sql, val)
        mydb.commit()
        aid=str(maxid)'''
        ##
        d1=detail.split('new google.maps.LatLng(')
        dlen=len(d1)
        
        d2=d1[1].split('),')
        #print(d2)
        location=d2[0]
        #print(location)
        loc=location.split(",")
        lat=loc[0]
        lon=loc[1]

        ##
        with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat="+lat+"&lon="+lon+"&appid=fe53b529190bb5029caf9b5e299d8503") as url:
            data = json.load(url)
            #print(data)
            json_object = json.dumps(data, indent=4)
             
            # Writing to sample.json
            with open("static/airdata.json", "w") as outfile:
                outfile.write(json_object)
        ##
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
                c1=data1['components']
                v1=c1['co']
                v2=c1['no']
                v3=c1['no2']
                v4=c1['o3']
                v5=c1['so2']
                v6=c1['pm2_5']
                v7=c1['pm10']
                v8=c1['nh3']
                air=str(v1)+","+str(v2)+","+str(v3)+","+str(v4)+","+str(v5)+","+str(v6)+","+str(v7)+","+str(v8)
                ff=open("static/air.txt","w")
                ff.write(air)
                ff.close()
                
            j+=1
        ##
        result=[]
        ff=open("static/air.txt","r")
        val=ff.read()
        ff.close()
        view=val.split(",")

        #print(view)
        
        n=5

        n1=float(view[0])
        n2=float(view[1])
        n3=float(view[2])
        n4=float(view[3])
        n5=float(view[4])
        
        a1=n1-n
        a2=n1+n

        b1=n2-n
        b2=n2+n

        c1=n3-n
        c2=n3+n

        d1=n4-n
        d2=n4+n

        e1=n5-n
        e2=n5+n
        ##########
        
        m1=470.0
        m2=448.0
        m3=468.0
        m4=176.0
        m5=196.0
        #if n1<=m1 and n2<=m2 and n3<=m3 and n4<=m4 and n5<=m5:
        act="1"
        x=(n1+n2+n3+n4+n5)/4
        print(x)
        if x <= 50:
            aq="Good"
            img="aq1.jpg"
        elif x <= 100:
            aq="Satisfactory"
            img="aq2.jpg"
        elif x <= 200:
            aq="Moderate"
            img="aq3.jpg"
        elif x <= 300:
            aq="Poor"
            img="aq4.jpg"
        elif x <= 400:
            aq="Very Poor"
            img="aq5.jpg"
        elif x > 400:
            aq="Severe"
            img="aq6.jpg"
        else:
            aq=""
        print(str(x))
        print(aq)
        xx=round(x,2)
        result.append(str(xx))
        result.append(aq)

        #if x>100:
        ax=round(x,2)
        mess="Pollution level "+aq+", AQI: "+str(ax)
        ##
        msg="ok"

    #mycursor.execute('SELECT * FROM air_geo_location order by id desc limit 0,1')
    #view1=mycursor.fetchall()
    #for view11 in view1:
    #    view=view11[2]

  
    return render_template('map1.html',msg=msg,view=view,result=result,img=img,mess=mess,mobile=mobile,name=name)

@app.route('/result', methods=['GET', 'POST'])
def result():
    msg=""
    result=[]
    ff=open("static/air.txt","r")
    val=ff.read()
    ff.close()
    view=val.split(",")

    print(view)
    
    n=5

    n1=float(view[0])
    n2=float(view[1])
    n3=float(view[2])
    n4=float(view[3])
    n5=float(view[4])
    
    a1=n1-n
    a2=n1+n

    b1=n2-n
    b2=n2+n

    c1=n3-n
    c2=n3+n

    d1=n4-n
    d2=n4+n

    e1=n5-n
    e2=n5+n
    ##########
    
    m1=470.0
    m2=448.0
    m3=468.0
    m4=176.0
    m5=196.0
    #if n1<=m1 and n2<=m2 and n3<=m3 and n4<=m4 and n5<=m5:
    act="1"
    x=(n1+n2+n3+n4+n5)/4
    print(x)
    if x <= 50:
        aq="Good"
    elif x <= 100:
        aq="Satisfactory"
    elif x <= 200:
        aq="Moderate"
    elif x <= 300:
        aq="Poor"
    elif x <= 400:
        aq="Very Poor"
    elif x > 400:
        aq="Severe"
    else:
        aq=""
    print(str(x))
    print(aq)
    xx=round(x,2)
    result.append(str(xx))
    result.append(aq)
    #else:
    #    act="2"
    #    msg="Incorrect Value!"
    
    #########
        
    '''x=0
    city_hour1=pd.read_csv('dataset/city_hour.csv')

    m1=470.0
    m2=448.0
    m3=468.0
    m4=176.0
    m5=196.0
    if n1<=m1 and n2<=m2 and n3<=m3 and n4<=m4 and n5<=m5:
        
        act="1"
        for ks5 in city_hour1.values:
            if ks5[4]>=a1 and ks5[4]<=a2 and ks5[5]>=b1 and ks5[5]<=b2 and ks5[6]>=c1 and ks5[6]<=c2 and ks5[8]>=d1 and ks5[8]<=d2 and ks5[9]>=e1 and ks5[9]<=e2:
                if pd.isnull(ks5[4]) and pd.isnull(ks5[5]) and pd.isnull(ks5[6]) and pd.isnull(ks5[8]) and pd.isnull(ks5[9]):
                    print("none")
                else:
                    result.append(ks5[2])
                    result.append(ks5[3])
                    result.append(ks5[7])
                    result.append(ks5[14])
                    result.append(ks5[15])
                    x+=1
                    break
               
    else:
        act="2"

    print("Result")
    print(result)
    if act=="1":
        if x>0:
            print("A")
            print(result[3])
            print(result[4])
        else:
            print("s")
            city_hour1=pd.read_csv('dataset/city_hour.csv')
            y1=0
            z1=0
            rn=randint(1,10)
            for ks4 in city_hour1.values:
                if ks4[0]==location:
                    
                    if pd.isnull(ks4[14]):
                        y1+=1
                    else:
                        if rn==z1:
                            result.append(ks4[2])
                            result.append(ks4[3])
                            result.append(ks4[7])
                            result.append(ks4[14])
                            result.append(ks4[15])
                            break
                        
                        z1+=1
    elif act=="2":
        msg="Incorrect Value!"'''
    

    return render_template('result.html',msg=msg,view=view,result=result)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    uname=""
    msg=""
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    
    
    return render_template('admin.html')

@app.route('/process1', methods=['GET', 'POST'])
def process1():
    uname=""
    msg=""
    file_arr=[]
    for dirname, _, filenames in os.walk('dataset'):
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            file_arr.append(filename)
            print(filename)


    path='dataset/'
    station_hour=pd.read_csv(path+'station_hour.csv')
    station_day=pd.read_csv(path+'station_day.csv')
    stations=pd.read_csv(path+'stations.csv')
    city_day=pd.read_csv(path+'city_day.csv')
    city_hour=pd.read_csv(path+'city_hour.csv')
    city=pd.read_csv(path+'Indian Cities Database.csv')


    #display("City In India")
    dat1=city.head()
    ##
    data1=[]
    for ss1 in dat1.values:
        data1.append(ss1)
    ##
    dat2=city.shape
    #print(dat2)

    #display("City Day in india")
    dat3=city_day.head()
    ##
    data3=[]
    for ss3 in dat3.values:
        data3.append(ss3)
    ##
    dat4=city_day.shape

    
    return render_template('process1.html',file_arr=file_arr,data1=data1,dat2=dat2,data3=data3,dat4=dat4)


#determined ht emissing data
def Missing (X):
    total = X.isnull().sum().sort_values(ascending = False)
    percent = round(X.isnull().sum().sort_values(ascending = False)/len(X)*100, 2)
    missing = pd.concat([total, percent], axis = 1,keys= ['Total', 'Percent'])
    
    return(missing) 
#plots number of dataframes side by side
def SideSide(*args):
    html_str=''
    dt=[]
    for df in args:
        html_str+=df.to_html()
        #val=df.to_html()
        #dt.append(val)
        
    #display_html(html_str.replace('table','table style="display:inline"'),raw = True)
    
@app.route('/process2', methods=['GET', 'POST'])
def process2():
    uname=""
    msg=""
    file_arr=[]
    for dirname, _, filenames in os.walk('dataset'):
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            file_arr.append(filename)
            print(filename)


    path='dataset/'
    station_hour=pd.read_csv(path+'station_hour.csv')
    station_day=pd.read_csv(path+'station_day.csv')
    stations=pd.read_csv(path+'stations.csv')
    city_day=pd.read_csv(path+'city_day.csv')
    city_hour=pd.read_csv(path+'city_hour.csv')
    city=pd.read_csv(path+'Indian Cities Database.csv')


    #display("City In India")
    dat1=city.head()
    ##
    #data1=[]
    #for ss1 in dat1.values:
    #    data1.append(ss1)
    ##
    dat2=city.shape
    
    dat3=city_day.head()
    
    dat4=city_day.shape

    #dat5=city_day.info()
    


    # Fill empty values with NaN
    city_day = city_day.fillna(np.nan)
    #finds missing values
    missing_city_day = Missing(city_day)
    
    print(missing_city_day)

    
    
    print('CITY DAY DATA')
    SideSide(missing_city_day)

    data1=[]
    dat=['Xylene','PM10','NH3','Toluene','Benzene','AQI_Bucket','AQI','PM2.5','NOx','O3','SO2','NO2','NO','CO','Date','City']
    i=0
    for ss1 in missing_city_day.values:
        d1=[]
        d1.append(dat[i])
        d1.append(ss1[0])
        d1.append(ss1[1])
        data1.append(d1)
        i+=1
    print(data1)
    
    #########
    print('\n\n  MISSING  DATA ')
    cmap = sns.diverging_palette( 220 , 10 , as_cmap = True )
    plt.figure(figsize = (20,8));
    sns.heatmap(city_day.isnull(), yticklabels = False, cbar = False, cmap = cmap)
    
    #plt.savefig('static/graph/graph1.png')
    #plt.show()
    plt.close()
    ###########
    #Cities in the dataset
    cities=city_day['City'].value_counts()
    #print('total number of cities in the dataset:',len(cities))
    #print(cities.index)
    len_city=len(cities)
    value='total number of cities in the dataset:'+str(len_city)
    data2=cities.index

    #Convert to Date Time format
    # Convert string to datetime 64
    city_day['Date']=pd.to_datetime(city_day['Date'])

    print(f"The available data is between {city_day['Date'].min()} and {city_day['Date'].max()}")

    #Analysing the Complete City Level Daily Data
    # combining the PM2.5 and PM10 into one column 
    city_day['Particulate_Matter']=city_day['PM2.5']+city_day['PM10']

    # Combining the Benezene ,Toulene and Xylene levels into one column
    city_day['poisionus']=city_day['Benzene']+city_day['Toluene']+city_day['Xylene']
    dat6=city_day.drop(['Benzene','Toluene','Xylene'],axis=1)
    data3=[]
    i=0
    rows=0
    cols=0
    rows=len(dat6.values)
    for ss3 in dat6.values:
        cols=len(ss3)
        data3.append(ss3)
        
    #####
    dat7=city_day['AQI_Bucket'].value_counts()
    data4=[]
    for ss4 in dat7.values:
        data4.append(ss4)
    print(data4)
    ######
    #sns.countplot(city_day['AQI_Bucket'])
    
    #plt.savefig('static/graph/graph2.png')
    #plt.show()
    plt.close()
    ####
    #data1=[]
    #value=[]
    #data2=[]
    #data3=[]
    #rows=0
    #cols=0
    #dat5=[]
    #data4=[]

    #,dat5=dat5
    return render_template('process2.html',data1=data1,value=value,data2=data2,data3=data3,rows=rows,cols=cols,data4=data4)

@app.route('/process3', methods=['GET', 'POST'])
def process3():
    uname=""
    msg=""
    file_arr=[]
    for dirname, _, filenames in os.walk('dataset'):
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            file_arr.append(filename)
            print(filename)


    path='dataset/'
    station_hour=pd.read_csv(path+'station_hour.csv')
    station_day=pd.read_csv(path+'station_day.csv')
    stations=pd.read_csv(path+'stations.csv')
    city_day=pd.read_csv(path+'city_day.csv')
    city_hour=pd.read_csv(path+'city_hour.csv')
    city=pd.read_csv(path+'Indian Cities Database.csv')


    #display("City In India")
    dat1=city.head()
    ##
    #data1=[]
    #for ss1 in dat1.values:
    #    data1.append(ss1)
    ##
    dat2=city.shape
    
    dat3=city_day.head()
    
    dat4=city_day.shape

    #dat5=city_day.info()
    


    # Fill empty values with NaN
    city_day = city_day.fillna(np.nan)
    #finds missing values
    missing_city_day = Missing(city_day)
    
    #print(missing_city_day)

    #print('CITY DAY DATA')
    SideSide(missing_city_day)

    #########
    #print('\n\n  MISSING  DATA ')
    cmap = sns.diverging_palette( 220 , 10 , as_cmap = True )
    #plt.figure(figsize = (20,8));
    #sns.heatmap(city_day.isnull(), yticklabels = False, cbar = False, cmap = cmap)
    
    #plt.savefig('static/graph/graph1.png')
    #plt.show()
    ###########
    #Cities in the dataset
    cities=city_day['City'].value_counts()
    #print('total number of cities in the dataset:',len(cities))
    #print(cities.index)

    value='total number of cities in the dataset:',len(cities)
    cities.index

    #Convert to Date Time format
    # Convert string to datetime 64
    city_day['Date']=pd.to_datetime(city_day['Date'])

    #print(f"The available data is between {city_day['Date'].min()} and {city_day['Date'].max()}")

    #Analysing the Complete City Level Daily Data
    # combining the PM2.5 and PM10 into one column 
    city_day['Particulate_Matter']=city_day['PM2.5']+city_day['PM10']

    # Combining the Benezene ,Toulene and Xylene levels into one column
    city_day['poisionus']=city_day['Benzene']+city_day['Toluene']+city_day['Xylene']
    dat6=city_day.drop(['Benzene','Toluene','Xylene'],axis=1)
    data3=[]
    i=0
    rows=0
    cols=0
    rows=len(dat6.values)
    for ss3 in dat6.values:
        cols=len(ss3)
        data3.append(ss3)
        
    
        
    #####
    city_day['AQI_Bucket'].value_counts()
    
    ######
    #sns.countplot(city_day['AQI_Bucket'])
    
    #plt.savefig('static/graph/graph2.png')
    #plt.show()
    ###################################
    #Visulising yearly data
    primary_pollutants=['PM2.5','PM10','NO2','NOx','CO','SO2']
    secondary_pollutants=['poisionus','O3']

    city_day.set_index('Date',inplace=True)
    #axes = city_day[primary_pollutants].plot(marker='.', alpha=0.5, linestyle='None', figsize=(16, 20), subplots=True)
    #for ax in axes:
        
    #    ax.set_xlabel('Years')
    #    ax.set_ylabel('ug / m3')
    #plt.savefig('static/graph/graph3.png')
    #plt.show()
    #plt.close()
    ##############
    temp=city_day.groupby('Date')[['PM2.5','PM10','NO2','NOx','CO','SO2']].sum().reset_index()
    temp=temp.melt(id_vars="Date",value_vars=['PM2.5','PM10','NO2','NOx','CO','SO2'],var_name='Pollutants',value_name='Count')
    temp.head()
    #fig=px.area(temp,x='Date',y='Count',color='Pollutants',height=600,title='Primary Pollutant over time',color_discrete_sequence=[cnf, dth, rec, act,wth,sth])
    #fig.update_layout(xaxis_rangeslider_visible=True)
    #plt.savefig('static/graph/graph4.png')
    #fig.show()
    #plt.close()

    #################
    temp=city_day.groupby('Date')[['poisionus','O3']].sum().reset_index()
    temp=temp.melt(id_vars="Date",value_vars=['poisionus','O3'],var_name='Pollutants',value_name='Count')
    temp.head()
    #fig=px.area(temp,x='Date',y='Count',color='Pollutants',height=600,title='Secondary Pollutant over time',color_discrete_sequence=[cnf, dth])
    #fig.update_layout(xaxis_rangeslider_visible=True)
    #fig.show()
    #plt.savefig('static/graph/graph5.png')
    #plt.close()
    #graph5
    ###########
    

    return render_template('process3.html',data3=data3,rows=rows,cols=cols)

#Feature Extraction
@app.route('/calculate_AQI', methods=['GET', 'POST'])
def calculate_AQI():
    # Missing values
    def missing_values(df):
            # Total missing values
            mis_val = df.isnull().sum()
            
            # Percentage of missing values
            mis_val_percent = 100 * df.isnull().sum() / len(df)
            
            # Make a table with the results
            mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
            
            # Rename the columns
            mis_val_table_ren_columns = mis_val_table.rename(columns = {0 : 'Missing Values', 1 : '% of Total Values'})
            
            # Sort the table by percentage of missing descending
            mis_val_table_ren_columns = mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
            
            # Print some summary information
            #print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"+"There are " + str(mis_val_table_ren_columns.shape[0]) +" columns that have missing values.")
            

            return mis_val_table_ren_columns.style.background_gradient(cmap='Reds')

    df_station_hour = pd.read_csv("dataset/station_hour.csv", parse_dates = ["Datetime"] )
    df_city_hour    = pd.read_csv("dataset/city_hour.csv")
    df_station_day  = pd.read_csv("dataset/station_day.csv")
    df_city_day     = pd.read_csv("dataset/city_day.csv")
    df_stations     = pd.read_csv("dataset/stations.csv")

    dat1=df_city_hour.head()
    #print(dat1)
    data1=[]
    for ss1 in dat1.values:
        data1.append(ss1)
    
    
    
    np.unique(df_city_hour['AQI_Bucket'][df_city_hour['AQI_Bucket'].notnull()].values)
    dat2=df_stations.head()
    data2=[]
    for ss2 in dat2.values:
        data2.append(ss2)

    grouped=df_stations.groupby(['State'])
    for name,group in grouped:
        print( name)
        print('-'*30)
        print( np.unique(group['City']),'\n\n')

    Amaravati=['AP001']
    df =df_station_hour



    df = df[df.StationId.isin(Amaravati)]
    df.sort_values(["StationId", "Datetime"], inplace = True)
    df["Date"] = df.Datetime.dt.date.astype(str)
    df.Datetime = df.Datetime.astype(str)

    dat3=df
    data3=[]
    for ss3 in dat3.values:
        data3.append(ss3)
    dat4=missing_values(df)
    #data4=[]
    #for ss4 in dat4:
    #    data4.append(ss4)

    df["PM10_24hr_avg"] = df.groupby("StationId")["PM10"].rolling(window = 24, min_periods = 16).mean().values
    df["PM2.5_24hr_avg"] = df.groupby("StationId")["PM2.5"].rolling(window = 24, min_periods = 16).mean().values
    df["SO2_24hr_avg"] = df.groupby("StationId")["SO2"].rolling(window = 24, min_periods = 16).mean().values
    df["NOx_24hr_avg"] = df.groupby("StationId")["NOx"].rolling(window = 24, min_periods = 16).mean().values
    df["NH3_24hr_avg"] = df.groupby("StationId")["NH3"].rolling(window = 24, min_periods = 16).mean().values
    df["CO_8hr_max"] = df.groupby("StationId")["CO"].rolling(window = 8, min_periods = 1).max().values
    df["O3_8hr_max"] = df.groupby("StationId")["O3"].rolling(window = 8, min_periods = 1).max().values
    print(df["O3_8hr_max"])
    ## PM2.5 Sub-Index calculation
    def get_PM25_subindex(x):
        if x <= 30:
            return x * 50 / 30
        elif x <= 60:
            return 50 + (x - 30) * 50 / 30
        elif x <= 90:
            return 100 + (x - 60) * 100 / 30
        elif x <= 120:
            return 200 + (x - 90) * 100 / 30
        elif x <= 250:
            return 300 + (x - 120) * 100 / 130
        elif x > 250:
            return 400 + (x - 250) * 100 / 130
        else:
            return 0

    df["PM2.5_SubIndex"] = df["PM2.5_24hr_avg"].apply(lambda x: get_PM25_subindex(x))
    ## PM10 Sub-Index calculation
    def get_PM10_subindex(x):
        if x <= 50:
            #return x * 50/ 50
            return x
        elif x <= 100:
            #return  50 + (x -  50) *  50 / 50
            return x
        elif x <= 250:
            return 100 + (x - 100) * 100 / 150
        elif x <= 350:
            return 200 + (x - 250)
        elif x <= 430:
            return 300 + (x - 350) * 100 / 80
        elif x > 430:
            return 400 + (x - 430) * 100 / 80
        else:
            return 0

    df["PM10_SubIndex"] = df["PM10_24hr_avg"].apply(lambda x: get_PM10_subindex(x))

    ## SO2 Sub-Index calculation
    def get_SO2_subindex(x):
        if x <= 40:
            return x * 50 / 40
        elif x <= 80:
            return 50 + (x - 40) * 50 / 40
        elif x <= 380:
            return 100 + (x - 80) * 100 / 300
        elif x <= 800:
            return 200 + (x - 380) * 100 / 420
        elif x <= 1600:
            return 300 + (x - 800) * 100 / 800
        elif x > 1600:
            return 400 + (x - 1600) * 100 / 800
        else:
            return 0

    df["SO2_SubIndex"] = df["SO2_24hr_avg"].apply(lambda x: get_SO2_subindex(x))

    ## NOx Sub-Index calculation
    def get_NOx_subindex(x):
        if x <= 40:
            return x * 50 / 40
        elif x <= 80:
            return 50 + (x - 40) * 50 / 40
        elif x <= 180:
            return 100 + (x - 80) * 100 / 100
        elif x <= 280:
            return 200 + (x - 180) * 100 / 100
        elif x <= 400:
            return 300 + (x - 280) * 100 / 120
        elif x > 400:
            return 400 + (x - 400) * 100 / 120
        else:
            return 0

    df["NOx_SubIndex"] = df["NOx_24hr_avg"].apply(lambda x: get_NOx_subindex(x))
    ## NH3 Sub-Index calculation
    def get_NH3_subindex(x):
        if x <= 200:
            return x * 50 / 200
        elif x <= 400:
            return 50 + (x - 200) * 50 / 200
        elif x <= 800:
            return 100 + (x - 400) * 100 / 400
        elif x <= 1200:
            return 200 + (x - 800) * 100 / 400
        elif x <= 1800:
            return 300 + (x - 1200) * 100 / 600
        elif x > 1800:
            return 400 + (x - 1800) * 100 / 600
        else:
            return 0

    df["NH3_SubIndex"] = df["NH3_24hr_avg"].apply(lambda x: get_NH3_subindex(x))
    ## CO Sub-Index calculation
    def get_CO_subindex(x):
        if x <= 1:
            return x * 50 / 1
        elif x <= 2:
            return 50 + (x - 1) * 50 / 1
        elif x <= 10:
            return 100 + (x - 2) * 100 / 8
        elif x <= 17:
            return 200 + (x - 10) * 100 / 7
        elif x <= 34:
            return 300 + (x - 17) * 100 / 17
        elif x > 34:
            return 400 + (x - 34) * 100 / 17
        else:
            return 0

    df["CO_SubIndex"] = df["CO_8hr_max"].apply(lambda x: get_CO_subindex(x))
    ## O3 Sub-Index calculation
    def get_O3_subindex(x):
        if x <= 50:
            return x * 50 / 50
        elif x <= 100:
            return 50 + (x - 50) * 50 / 50
        elif x <= 168:
            return 100 + (x - 100) * 100 / 68
        elif x <= 208:
            return 200 + (x - 168) * 100 / 40
        elif x <= 748:
            return 300 + (x - 208) * 100 / 539
        elif x > 748:
            return 400 + (x - 400) * 100 / 539
        else:
            return 0

    df["O3_SubIndex"] = df["O3_8hr_max"].apply(lambda x: get_O3_subindex(x))
    ## AQI bucketing
    def get_AQI_bucket(x):
        if x <= 50:
            return "Good"
        elif x <= 100:
            return "Satisfactory"
        elif x <= 200:
            return "Moderate"
        elif x <= 300:
            return "Poor"
        elif x <= 400:
            return "Very Poor"
        elif x > 400:
            return "Severe"
        else:
            return np.nan

    df["Checks"] = (df["PM2.5_SubIndex"] > 0).astype(int) + \
                    (df["PM10_SubIndex"] > 0).astype(int) + \
                    (df["SO2_SubIndex"] > 0).astype(int) + \
                    (df["NOx_SubIndex"] > 0).astype(int) + \
                    (df["NH3_SubIndex"] > 0).astype(int) + \
                    (df["CO_SubIndex"] > 0).astype(int) + \
                    (df["O3_SubIndex"] > 0).astype(int)

    df["AQI_calculated"] = round(df[["PM2.5_SubIndex", "PM10_SubIndex", "SO2_SubIndex", "NOx_SubIndex",
                                     "NH3_SubIndex", "CO_SubIndex", "O3_SubIndex"]].max(axis = 1))
    df.loc[df["PM2.5_SubIndex"] + df["PM10_SubIndex"] <= 0, "AQI_calculated"] = np.nan
    df.loc[df.Checks < 3, "AQI_calculated"] = np.nan

    df["AQI_bucket_calculated"] = df["AQI_calculated"].apply(lambda x: get_AQI_bucket(x))
    dat5=df[~df.AQI_calculated.isna()].head(13)
    #print(dat5)
    data5=[]
    for ss5 in dat5.values:
        
        data5.append(ss5)

    #######################################################################
    path='dataset/'
    station_hour=pd.read_csv(path+'station_hour.csv')
    station_day=pd.read_csv(path+'station_day.csv')
    stations=pd.read_csv(path+'stations.csv')
    city_day=pd.read_csv(path+'city_day.csv')
    city_hour=pd.read_csv(path+'city_hour.csv')
    city=pd.read_csv(path+'Indian Cities Database.csv')


    #display("City In India")
    dat1=city.head()
    ##
    #data1=[]
    #for ss1 in dat1.values:
    #    data1.append(ss1)
    ##
    dat2=city.shape
    
    dat3=city_day.head()
    
    dat4=city_day.shape

    #dat5=city_day.info()
    


    # Fill empty values with NaN
    city_day = city_day.fillna(np.nan)
    #finds missing values
    missing_city_day = Missing(city_day)
    
    #print(missing_city_day)

    #print('CITY DAY DATA')
    SideSide(missing_city_day)

    #########
    #print('\n\n  MISSING  DATA ')
    cmap = sns.diverging_palette( 220 , 10 , as_cmap = True )
    #plt.figure(figsize = (20,8));
    #sns.heatmap(city_day.isnull(), yticklabels = False, cbar = False, cmap = cmap)
    
    #plt.savefig('static/graph/graph1.png')
    #plt.show()
    #plt.close()
    ###########
    #Cities in the dataset
    cities=city_day['City'].value_counts()
    #print('total number of cities in the dataset:',len(cities))
    #print(cities.index)

    value='total number of cities in the dataset:',len(cities)
    cities.index

    #Convert to Date Time format
    # Convert string to datetime 64
    city_day['Date']=pd.to_datetime(city_day['Date'])

    #print(f"The available data is between {city_day['Date'].min()} and {city_day['Date'].max()}")

    #Analysing the Complete City Level Daily Data
    # combining the PM2.5 and PM10 into one column 
    city_day['Particulate_Matter']=city_day['PM2.5']+city_day['PM10']

    # Combining the Benezene ,Toulene and Xylene levels into one column
    city_day['poisionus']=city_day['Benzene']+city_day['Toluene']+city_day['Xylene']
    dat6=city_day.drop(['Benzene','Toluene','Xylene'],axis=1)
    data33=[]
    i=0
    rows=0
    cols=0
    rows=len(dat6.values)
    for ss33 in dat6.values:
        cols=len(ss33)
        data33.append(ss3)
        
    
        
    #####
    city_day['AQI_Bucket'].value_counts()
    
    ######
    #sns.countplot(city_day['AQI_Bucket'])
    
    #plt.savefig('static/graph/graph2.png')
    #plt.show()
    #plt.close()
    ###################################
    #Visulising yearly data
    primary_pollutants=['PM2.5','PM10','NO2','NOx','CO','SO2']
    secondary_pollutants=['poisionus','O3']

    city_day.set_index('Date',inplace=True)
    #axes = city_day[primary_pollutants].plot(marker='.', alpha=0.5, linestyle='None', figsize=(16, 20), subplots=True)
    #for ax in axes:
        
    #    ax.set_xlabel('Years')
    #    ax.set_ylabel('ug / m3')
    #plt.savefig('static/graph/graph3.png')
    #plt.show()
    ##############
    temp=city_day.groupby('Date')[['PM2.5','PM10','NO2','NOx','CO','SO2']].sum().reset_index()
    temp=temp.melt(id_vars="Date",value_vars=['PM2.5','PM10','NO2','NOx','CO','SO2'],var_name='Pollutants',value_name='Count')
    temp.head()
    fig=px.area(temp,x='Date',y='Count',color='Pollutants',height=600,title='Primary Pollutant over time',color_discrete_sequence=[cnf, dth, rec, act,wth,sth])
    fig.update_layout(xaxis_rangeslider_visible=True)
    #plt.savefig('static/graph/graph4.png')
    #fig.show()

    #################
    temp=city_day.groupby('Date')[['poisionus','O3']].sum().reset_index()
    temp=temp.melt(id_vars="Date",value_vars=['poisionus','O3'],var_name='Pollutants',value_name='Count')
    temp.head()
    fig=px.area(temp,x='Date',y='Count',color='Pollutants',height=600,title='Secondary Pollutant over time',color_discrete_sequence=[cnf, dth])
    fig.update_layout(xaxis_rangeslider_visible=True)
    #fig.show()
    #graph5
    ###########
    def trend_plot(dataframe,value):
    
        # Prepare data
        df['year'] = [d.year for d in df.Date]
        df['month'] = [d.strftime('%b') for d in df.Date]
        years = df['year'].unique()

        # Draw Plot
        fig, axes = plt.subplots(1, 2, figsize=(14,6), dpi= 80)
        sns.boxplot(x='year', y=value, data=df, ax=axes[0])
        sns.pointplot(x='month', y=value, data=df.loc[~df.year.isin([2015, 2020]), :])

        # Set Title
        axes[0].set_title('Year-wise Box Plot \n(The Trend)', fontsize=18); 
        axes[1].set_title('Month-wise Plot \n(The Seasonality)', fontsize=18)
        plt.show()
    city_day.reset_index(inplace=True)
    df = city_day.copy()
    value='NO2'
    #trend_plot(df,value)
    #graph6
    ###################

    city_day.reset_index(inplace=True)
    df = city_day.copy()
    value='PM10'
    #trend_plot(df,value)
    #graph7
    ###########################
    city_day.reset_index(inplace=True)
    df = city_day.copy()
    value='poisionus'
    #trend_plot(df,value)
    
    #graph8
    #######################
    def max_polluted_city(pollutant):
        x1 = city_day[[pollutant,'City']].groupby(["City"]).mean().sort_values(by=pollutant,ascending=False).reset_index()
        x1[pollutant] = round(x1[pollutant],2)
        return x1[:10].style.background_gradient(cmap='OrRd')

    #source: https://stackoverflow.com/questions/38783027/jupyter-notebook-display-two-pandas-tables-side-by-side
    #from IPython.display import display_html
    def display_side_by_side(*args):
        html_str=''
        for df in args:
            html_str+=df.render()
        display_html(html_str.replace('table','table style="display:inline"'),raw=True)
    
    pm2_5 = max_polluted_city('PM2.5')
    pm10 = max_polluted_city('PM10')
    no2 = max_polluted_city('NO2')
    so2 = max_polluted_city('SO2')
    co = max_polluted_city('CO')
    posinious = max_polluted_city('poisionus')


    #display_side_by_side(pm2_5,pm10,no2,so2,co,posinious)
    #############

    '''dat6=df[~df.AQI_calculated.isna()].AQI_bucket_calculated.value_counts()
    print(dat6)

    df_check_station_hour = df1[["AQI", "AQI_calculated"]].dropna()
    print("Station + Hour")
    print("Rows: ", df_check_station_hour.shape[0])
    print("Matched AQI: ", (df_check_station_hour.AQI == df_check_station_hour.AQI_calculated).sum())
    print("% Match: ", (df_check_station_hour.AQI == df_check_station_hour.AQI_calculated).sum() * 100 / df_check_station_hour.shape[0])'''
    ##########
    ###
    full_grouped=city_day.groupby(['Date','City',])[['PM2.5','PM10','NO2','NOx','CO','SO2','poisionus','O3','AQI']].sum().reset_index()
    day_wise=full_grouped.groupby('Date')[['NO2','AQI']].sum().reset_index()
    day_wise['No.of city']=full_grouped[full_grouped['NO2']!=0].groupby('Date')['City'].unique().apply(len).values
    day_wise['No.of City']=full_grouped[full_grouped['AQI']!=0].groupby('Date')['City'].unique().apply(len).values
    fig_c=px.line(day_wise,x="Date",y="NO2",color_discrete_sequence=[act])
    fig_d=px.line(day_wise,x="Date",y="AQI",color_discrete_sequence=[dth])
    fig=make_subplots(rows=1,cols=2,shared_xaxes=False,horizontal_spacing=0.1,subplot_titles=('NO2 Present in Air','AQI'))
    fig.add_trace(fig_c['data'][0],row=1,col=1)
    fig.add_trace(fig_d['data'][0],row=1,col=2)
    fig.update_layout(height=460)
    #fig.show()
    #graph9
    ##############
    City_wise=full_grouped[full_grouped['Date']==max(full_grouped['Date'])].reset_index(drop=True).drop('Date',axis=1)
    #group by City
    City_wise=City_wise.groupby('City')[['NO2','AQI']].sum().reset_index()
    fig=px.scatter(City_wise.sort_values('AQI',ascending=False).iloc[:15,:],x="AQI",y='NO2',color='City',size='AQI',height=700,text='City',log_x=True,log_y=True,title="NO2 Vs AQI (Scale is in log10)")
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_rangeslider_visible=True)
    #fig.show()
    #graph10
    ###########
    City_wise=full_grouped[full_grouped['Date']==max(full_grouped['Date'])].reset_index(drop=True).drop('Date',axis=1)
    #group by City
    City_wise=City_wise.groupby('City')[['AQI','poisionus']].sum().reset_index()
    fig=px.scatter(City_wise.sort_values('AQI',ascending=False).iloc[:15,:],x="AQI",y='poisionus',color='City',size='AQI',height=700,text='City',log_x=True,log_y=True,title="Poisionus Vs AQI (Scale is in log10)")
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_rangeslider_visible=True)
    #fig.show()
    #graph11
    #################
    #AQI for some of the major cities of India
    cities = ['Ahmedabad','Delhi','Bengaluru','Mumbai','Hyderabad','Chennai']

    filtered_city_day = city_day[city_day['Date'] >= '2019-01-01']
    AQI = filtered_city_day[filtered_city_day.City.isin(cities)][['Date','City','AQI','AQI_Bucket']]
    dat7=AQI.head()
    data7=[]
    dtn=['1461','1462','1463','1464','1465']
    i=0
    for ss7 in dat7.values:
        dt2=[]
        dt2.append(dtn[i])
        dt2.append(ss7[0])
        dt2.append(ss7[1])
        dt2.append(ss7[2])
        dt2.append(ss7[3])
        
        data7.append(dt2)
        i+=1
    ##############
    fig=px.line(full_grouped,x='Date',y='AQI',color='City',height=600,title='AQI',color_discrete_sequence=px.colors.cyclical.mygbm)
    #fig.show()
    #graph12
    ###############
    full_latest=city_day[city_day['Date']==max(city_day['Date'])]
    fig=px.treemap(full_latest.sort_values(by='AQI',ascending=False).reset_index(drop=True),path=["City"],values='AQI',height=700,title="AOI of City",color_discrete_sequence=px.colors.qualitative.Dark2)
    fig.data[0].textinfo='label+text+value'
    #fig.show()
    #graph13
    ###########
    '''AQI_pivot = AQI.pivot(index='Date', columns='City', values='AQI')
    AQI_pivot.fillna(method='bfill',inplace=True)
    #Source code for racing barchart: https://github.com/dexplo/bar_chart_race
    AQI_2020 = AQI_pivot[AQI_pivot.index > '2019-12-31']
    bcr_html = bcr.bar_chart_race(df=AQI_2020, filename=None, period_length=300,orientation='v',figsize=(8, 6),bar_label_size=7,tick_label_size=7,title='AQI levels in 2020')
    display_html(bcr_html)'''





        

    return render_template('calculate_AQI.html',data1=data1,data2=data2,data3=data3,data5=data5,data7=data7)


##LSTM
def load_data(stock, seq_len):
    amount_of_features = len(stock.columns)
    data = stock.as_matrix() #pd.DataFrame(stock)
    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])

    result = np.array(result)
    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    x_train = train[:, :-1]
    y_train = train[:, -1][:,-1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1][:,-1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], amount_of_features))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], amount_of_features))  

    return [x_train, y_train, x_test, y_test]

def build_model(layers):
    model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[2]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop",metrics=['accuracy'])
    print("Compilation Time : ", time.time() - start)
    return model

def build_model2(layers):
        d = 0.2
        model = Sequential()
        model.add(LSTM(128, input_shape=(layers[1], layers[0]), return_sequences=True))
        model.add(Dropout(d))
        model.add(LSTM(64, input_shape=(layers[1], layers[0]), return_sequences=False))
        model.add(Dropout(d))
        model.add(Dense(16,init='uniform',activation='relu'))        
        model.add(Dense(1,init='uniform',activation='linear'))
        model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
        return model


#Classification
@app.route('/classification', methods=['GET', 'POST'])
def classification():
    
    #######################################################################
    path='dataset/'
    station_hour=pd.read_csv(path+'station_hour.csv')
    station_day=pd.read_csv(path+'station_day.csv')
    stations=pd.read_csv(path+'stations.csv')
    city_day=pd.read_csv(path+'city_day.csv')
    city_hour=pd.read_csv(path+'city_hour.csv')
    city=pd.read_csv(path+'Indian Cities Database.csv')


    #display("City In India")
    dat1=city.head()
    ##
    mycursor = mydb.cursor()
    
    ###########    
    '''data11=[]
    for ss11 in city.values:
        mycursor.execute("SELECT max(id)+1 FROM air_location")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        
        
        sql = "INSERT INTO air_location(id, city,lat,lon,country,iso2,state) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        val = (maxid,ss11[0],ss11[1],ss11[2],ss11[3],ss11[4],ss11[5])
        act="success"
        mycursor.execute(sql, val)
        mydb.commit() '''    
    ##########
    
    dat2=city.shape
    
    dat3=city_day.head()
    
    dat4=city_day.shape

    #dat5=city_day.info()
    


    # Fill empty values with NaN
    city_day = city_day.fillna(np.nan)
    #finds missing values
    missing_city_day = Missing(city_day)
    
    #print(missing_city_day)

    #print('CITY DAY DATA')
    SideSide(missing_city_day)

    #########
    #print('\n\n  MISSING  DATA ')
    cmap = sns.diverging_palette( 220 , 10 , as_cmap = True )
    #plt.figure(figsize = (20,8));
    #sns.heatmap(city_day.isnull(), yticklabels = False, cbar = False, cmap = cmap)
    
    #plt.savefig('static/graph/graph1.png')
    #plt.show()
    ###########
    #Cities in the dataset
    cities=city_day['City'].value_counts()
    #print('total number of cities in the dataset:',len(cities))
    #print(cities.index)

    value='total number of cities in the dataset:',len(cities)
    cities.index

    #Convert to Date Time format
    # Convert string to datetime 64
    city_day['Date']=pd.to_datetime(city_day['Date'])

    #print(f"The available data is between {city_day['Date'].min()} and {city_day['Date'].max()}")

    #Analysing the Complete City Level Daily Data
    # combining the PM2.5 and PM10 into one column 
    city_day['Particulate_Matter']=city_day['PM2.5']+city_day['PM10']

    # Combining the Benezene ,Toulene and Xylene levels into one column
    city_day['poisionus']=city_day['Benzene']+city_day['Toluene']+city_day['Xylene']
    dat6=city_day.drop(['Benzene','Toluene','Xylene'],axis=1)
    
        
    #####
    #print(city_day['AQI_Bucket'])
    dat7=city_day['AQI_Bucket'].value_counts()
    data4=[]
    for ss4 in dat7.values:
        data4.append(ss4)
    print(data4)
    ######
    #sns.countplot(city_day['AQI_Bucket'])
    
    #plt.savefig('static/graph/graph2.png')
    #plt.show()
    ###################################
    #Visulising yearly data
    primary_pollutants=['PM2.5','PM10','NO2','NOx','CO','SO2']
    secondary_pollutants=['poisionus','O3']

    city_day.set_index('Date',inplace=True)
    #axes = city_day[primary_pollutants].plot(marker='.', alpha=0.5, linestyle='None', figsize=(16, 20), subplots=True)
    #for ax in axes:
        
    #    ax.set_xlabel('Years')
    #    ax.set_ylabel('ug / m3')
    #plt.savefig('static/graph/graph3.png')
    #plt.show()
    ##############
    temp=city_day.groupby('Date')[['PM2.5','PM10','NO2','NOx','CO','SO2']].sum().reset_index()
    temp=temp.melt(id_vars="Date",value_vars=['PM2.5','PM10','NO2','NOx','CO','SO2'],var_name='Pollutants',value_name='Count')
    temp.head()
    fig=px.area(temp,x='Date',y='Count',color='Pollutants',height=600,title='Primary Pollutant over time',color_discrete_sequence=[cnf, dth, rec, act,wth,sth])
    fig.update_layout(xaxis_rangeslider_visible=True)
    #plt.savefig('static/graph/graph4.png')
    #fig.show()

    #################
    temp=city_day.groupby('Date')[['poisionus','O3']].sum().reset_index()
    temp=temp.melt(id_vars="Date",value_vars=['poisionus','O3'],var_name='Pollutants',value_name='Count')
    temp.head()
    fig=px.area(temp,x='Date',y='Count',color='Pollutants',height=600,title='Secondary Pollutant over time',color_discrete_sequence=[cnf, dth])
    fig.update_layout(xaxis_rangeslider_visible=True)
    #fig.show()
    #graph5
    ###########
    def trend_plot(dataframe,value):
    
        # Prepare data
        df['year'] = [d.year for d in df.Date]
        df['month'] = [d.strftime('%b') for d in df.Date]
        years = df['year'].unique()

        # Draw Plot
        fig, axes = plt.subplots(1, 2, figsize=(14,6), dpi= 80)
        sns.boxplot(x='year', y=value, data=df, ax=axes[0])
        sns.pointplot(x='month', y=value, data=df.loc[~df.year.isin([2015, 2020]), :])

        # Set Title
        axes[0].set_title('Year-wise Box Plot \n(The Trend)', fontsize=18); 
        axes[1].set_title('Month-wise Plot \n(The Seasonality)', fontsize=18)
        plt.show()
    city_day.reset_index(inplace=True)
    df = city_day.copy()
    value='NO2'
    #trend_plot(df,value)
    #graph6
    ###################

    city_day.reset_index(inplace=True)
    df = city_day.copy()
    value='PM10'
    #trend_plot(df,value)
    #graph7
    ###########################
    city_day.reset_index(inplace=True)
    df = city_day.copy()
    value='poisionus'
    #trend_plot(df,value)
    #graph8
    #######################
    def max_polluted_city(pollutant):
        x1 = city_day[[pollutant,'City']].groupby(["City"]).mean().sort_values(by=pollutant,ascending=False).reset_index()
        x1[pollutant] = round(x1[pollutant],2)
        return x1[:10].style.background_gradient(cmap='OrRd')

    #source: https://stackoverflow.com/questions/38783027/jupyter-notebook-display-two-pandas-tables-side-by-side
    #from IPython.display import display_html
    def display_side_by_side(*args):
        html_str=''
        for df in args:
            html_str+=df.render()
        display_html(html_str.replace('table','table style="display:inline"'),raw=True)
    
    pm2_5 = max_polluted_city('PM2.5')
    pm10 = max_polluted_city('PM10')
    no2 = max_polluted_city('NO2')
    so2 = max_polluted_city('SO2')
    co = max_polluted_city('CO')
    posinious = max_polluted_city('poisionus')


    #display_side_by_side(pm2_5,pm10,no2,so2,co,posinious)
    #############

    '''dat6=df[~df.AQI_calculated.isna()].AQI_bucket_calculated.value_counts()
    print(dat6)

    df_check_station_hour = df1[["AQI", "AQI_calculated"]].dropna()
    print("Station + Hour")
    print("Rows: ", df_check_station_hour.shape[0])
    print("Matched AQI: ", (df_check_station_hour.AQI == df_check_station_hour.AQI_calculated).sum())
    print("% Match: ", (df_check_station_hour.AQI == df_check_station_hour.AQI_calculated).sum() * 100 / df_check_station_hour.shape[0])'''
    ##########
    ###
    full_grouped=city_day.groupby(['Date','City',])[['PM2.5','PM10','NO2','NOx','CO','SO2','poisionus','O3','AQI']].sum().reset_index()
    day_wise=full_grouped.groupby('Date')[['NO2','AQI']].sum().reset_index()
    day_wise['No.of city']=full_grouped[full_grouped['NO2']!=0].groupby('Date')['City'].unique().apply(len).values
    day_wise['No.of City']=full_grouped[full_grouped['AQI']!=0].groupby('Date')['City'].unique().apply(len).values
    fig_c=px.line(day_wise,x="Date",y="NO2",color_discrete_sequence=[act])
    fig_d=px.line(day_wise,x="Date",y="AQI",color_discrete_sequence=[dth])
    fig=make_subplots(rows=1,cols=2,shared_xaxes=False,horizontal_spacing=0.1,subplot_titles=('NO2 Present in Air','AQI'))
    fig.add_trace(fig_c['data'][0],row=1,col=1)
    fig.add_trace(fig_d['data'][0],row=1,col=2)
    fig.update_layout(height=460)
    #fig.show()
    #graph9
    ##############
    City_wise=full_grouped[full_grouped['Date']==max(full_grouped['Date'])].reset_index(drop=True).drop('Date',axis=1)
    #group by City
    City_wise=City_wise.groupby('City')[['NO2','AQI']].sum().reset_index()
    fig=px.scatter(City_wise.sort_values('AQI',ascending=False).iloc[:15,:],x="AQI",y='NO2',color='City',size='AQI',height=700,text='City',log_x=True,log_y=True,title="NO2 Vs AQI (Scale is in log10)")
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_rangeslider_visible=True)
    #fig.show()
    #graph10
    ###########
    City_wise=full_grouped[full_grouped['Date']==max(full_grouped['Date'])].reset_index(drop=True).drop('Date',axis=1)
    #group by City
    City_wise=City_wise.groupby('City')[['AQI','poisionus']].sum().reset_index()
    fig=px.scatter(City_wise.sort_values('AQI',ascending=False).iloc[:15,:],x="AQI",y='poisionus',color='City',size='AQI',height=700,text='City',log_x=True,log_y=True,title="Poisionus Vs AQI (Scale is in log10)")
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_rangeslider_visible=True)
    #fig.show()
    #graph11
    #################
    #AQI for some of the major cities of India
    cities = ['Chennai','Delhi','Bengaluru','Mumbai','Hyderabad','Ahmedabad']

    filtered_city_day = city_day[city_day['Date'] >= '2019-01-01']
    AQI = filtered_city_day[filtered_city_day.City.isin(cities)][['Date','City','AQI','AQI_Bucket']]
    dat7=AQI.head()
    data7=[]
    dtn=['1461','1462','1463','1464','1465']
    i=0
    for ss7 in dat7.values:
        dt2=[]
        dt2.append(dtn[i])
        dt2.append(ss7[0])
        dt2.append(ss7[1])
        dt2.append(ss7[2])
        dt2.append(ss7[3])
        
        data7.append(dt2)
        i+=1
    ##############
    fig=px.line(full_grouped,x='Date',y='AQI',color='City',height=600,title='AQI',color_discrete_sequence=px.colors.cyclical.mygbm)
    #fig.show()
    #graph12
    ###############
    full_latest=city_day[city_day['Date']==max(city_day['Date'])]
    fig=px.treemap(full_latest.sort_values(by='AQI',ascending=False).reset_index(drop=True),path=["City"],values='AQI',height=700,title="AOI of City",color_discrete_sequence=px.colors.qualitative.Dark2)
    fig.data[0].textinfo='label+text+value'
    #fig.show()
    #graph13
    ###########
    AQI_pivot = AQI.pivot(index='Date', columns='City', values='AQI')
    AQI_pivot.fillna(method='bfill',inplace=True)
    #Source code for racing barchart: https://github.com/dexplo/bar_chart_race
    AQI_2020 = AQI_pivot[AQI_pivot.index > '2019-12-31']
    #bcr_html = bcr.bar_chart_race(df=AQI_2020, filename=None, period_length=300,orientation='v',figsize=(8, 6),bar_label_size=7,tick_label_size=7,title='AQI levels in 2020')
    #display_html(bcr_html)

    ##########
    AQI_beforeLockdown = AQI_pivot['2020-01-01':'2020-03-25']
    AQI_afterLockdown = AQI_pivot['2020-03-26':'2020-05-01']

    print(AQI_beforeLockdown.mean())
    print(AQI_afterLockdown.mean())
    # Helper functions

    #######
    mycursor.execute("SELECT * FROM air_location")
    loc_data = mycursor.fetchall()

    ###############
    '''for ds1 in loc_data:
        
        res=get_AQI_classify(ds1[1])
        mycursor.execute("update air_location set aqi=%s,aqi_bucket=%s where city=%s",(res[0],res[1],ds1[1]))
        mydb.commit()'''
    #############
    
    return render_template('classification.html',data4=data4,loc_data=loc_data)


def get_AQI_classify(location):
        x=0
        x1=0
        y1=0
        z1=0
        s1=0
        val=[]
        city_hour1=pd.read_csv('dataset/city_hour.csv')
        for ks5 in city_hour1.values:
            if ks5[0]==location:
                x1+=1
                if pd.isnull(ks5[14]):
                    y1+=1
                else:
                    s1+=ks5[14]
                    z1+=1

        if z1>0:        
            aqi1=s1/z1
            x=int(aqi1)
            
            if x <= 50:
                aq="Good"
            elif x <= 100:
                aq="Satisfactory"
            elif x <= 200:
                aq="Moderate"
            elif x <= 300:
                aq="Poor"
            elif x <= 400:
                aq="Very Poor"
            elif x > 400:
                aq="Severe"
            else:
                aq=""
        else:
            x=0
            aq=""

        val.append(x)
        val.append(aq)
        return val

@app.route('/test_search', methods=['GET', 'POST'])
def test_search():
    uname=""
    msg=""
    act=""
    result=[]
    value=[]
    loc = request.args.get('loc')


    mycursor = mydb.cursor()

    
    

    if request.method == 'POST':
        nn1 = request.form['n1']
        nn2 = request.form['n2']
        nn3 = request.form['n3']
        nn4 = request.form['n4']
        nn5 = request.form['n5']
        loc1 = request.form['loc1']

        locc="%"+loc1+"%"
        mycursor.execute("SELECT * FROM air_location where city like %s",(locc,))
        value = mycursor.fetchone()
        location=value[1]
    
        n=5

        n1=float(nn1)
        n2=float(nn2)
        n3=float(nn3)
        n4=float(nn4)
        n5=float(nn5)
        
        a1=n1-n
        a2=n1+n

        b1=n2-n
        b2=n2+n

        c1=n3-n
        c2=n3+n

        d1=n4-n
        d2=n4+n

        e1=n5-n
        e2=n5+n
        ##########
        '''
        m1=470.0
        m2=448.0
        m3=468.0
        m4=176.0
        m5=196.0
        if n1<=m1 and n2<=m2 and n3<=m3 and n4<=m4 and n5<=m5:
            act="1"
            x=(n1+n2+n3+n4+n5)/4
            if x <= 50:
                aq="Good"
            elif x <= 100:
                aq="Satisfactory"
            elif x <= 200:
                aq="Moderate"
            elif x <= 300:
                aq="Poor"
            elif x <= 400:
                aq="Very Poor"
            elif x > 400:
                aq="Severe"
            else:
                aq=""
            result.append(str(x))
            result.append(aq)
        else:
            act="2"
            msg="Incorrect Value!"
        '''
        #########
        
        x=0
        city_hour1=pd.read_csv('dataset/city_hour.csv')

        m1=470.0
        m2=448.0
        m3=468.0
        m4=176.0
        m5=196.0
        if n1<=m1 and n2<=m2 and n3<=m3 and n4<=m4 and n5<=m5:
            
            act="1"
            for ks5 in city_hour1.values:
                if ks5[4]>=a1 and ks5[4]<=a2 and ks5[5]>=b1 and ks5[5]<=b2 and ks5[6]>=c1 and ks5[6]<=c2 and ks5[8]>=d1 and ks5[8]<=d2 and ks5[9]>=e1 and ks5[9]<=e2:
                    if pd.isnull(ks5[4]) and pd.isnull(ks5[5]) and pd.isnull(ks5[6]) and pd.isnull(ks5[8]) and pd.isnull(ks5[9]):
                        print("none")
                    else:
                        result.append(ks5[2])
                        result.append(ks5[3])
                        result.append(ks5[7])
                        result.append(ks5[14])
                        result.append(ks5[15])
                        x+=1
                        break
                   
        else:
            act="2"

        print("Result")
        print(result)
        if act=="1":
            if x>0:
                print("A")
                print(result[3])
                print(result[4])
            else:
                print("s")
                city_hour1=pd.read_csv('dataset/city_hour.csv')
                y1=0
                z1=0
                rn=randint(1,10)
                for ks4 in city_hour1.values:
                    if ks4[0]==location:
                        
                        if pd.isnull(ks4[14]):
                            y1+=1
                        else:
                            if rn==z1:
                                result.append(ks4[2])
                                result.append(ks4[3])
                                result.append(ks4[7])
                                result.append(ks4[14])
                                result.append(ks4[15])
                                break
                            
                            z1+=1
        elif act=="2":
            msg="Incorrect Value!"

        
    
    return render_template('test_search.html',act=act,msg=msg,result=result,value=value,loc=loc)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)

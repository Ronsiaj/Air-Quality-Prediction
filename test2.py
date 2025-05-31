import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df1= pd.read_csv('static/dataset/city_day.csv')

dat1=df1.head()
#print(dat1)
df1['City'].unique()
df = df1[df1['City']=='Delhi']
dat2=df.head()
#print(dat2)
dat3=df.shape
print(dat3)
#df.info()
df.isnull().sum()
df= df.drop(['Xylene','Toluene','Benzene','O3','CO','SO2'], axis=1)
df1['City'].unique()
df = df.dropna()
df2 = df1[df1['City']=='Mumbai']
sns.heatmap(df.corr())

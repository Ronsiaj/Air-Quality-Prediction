# importing package
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
# create data
'''df = pd.DataFrame([['A', 10, 20, 10, 26], ['B', 20, 25, 15, 21], ['C', 12, 15, 19, 6],
                   ['D', 10, 18, 11, 19]],
                  columns=['Team', 'Round 1', 'Round 2', 'Round 3', 'Round 4'])
# view data
print(df)
 
# plot data in stack manner of bar type
df.plot(x='Team', kind='bar', stacked=True,
        title='Stacked Bar Graph by dataframe')
plt.show()'''
c=['red','green','blue','yellow','orange','pink','brown']
df = pd.DataFrame([['AQI', 50, 100, 200, 300, 400, 500], ['Predicted', 120]],columns=['AQI', 'Good', 'Satisfactory', 'Moderate', 'Poor','Very Poor','Severe'])
# view data
print(df)
 
# plot data in stack manner of bar type
df.plot(x='AQI', kind='bar', stacked=False,
        title='Stacked Bar Graph by dataframe')

plt.xticks(rotation=0)
plt.show()

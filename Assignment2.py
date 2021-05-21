
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[22]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.dates as dates
import matplotlib.ticker as ticker





# In[23]:

get_ipython().magic('matplotlib notebook')
get_ipython().magic('matplotlib inline')

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')#size: 165085 rows × 4 columns
df['Data_Value']=df['Data_Value']*0.1
df['Date']=pd.to_datetime(df['Date'])
df_2015=df[(df['Date'].dt.year)==2015]
df=df[(df['Date'].dt.year)>=2005]
df=df[(df['Date'].dt.year)<=2014]
df['Month_Day']= df['Date'].dt.strftime('%m-%d')
df= df[df['Month_Day']!='02-29']

#Max and Min data
df_tmax=df[df['Element']=='TMAX']#size: 83063 rows × 4 columns
df_tmin=df[df['Element']=='TMIN'] #size: 82022 rows × 4 columns
df_tmax=pd.DataFrame(df_tmax.groupby(['Month_Day'])['Data_Value'].max())
df_tmin=pd.DataFrame(df_tmin.groupby(['Month_Day'])['Data_Value'].min())

#2015 record breaking data
df_2015['Month_Day']= df_2015['Date'].dt.strftime('%m-%d')
df_2015= df_2015[df_2015['Month_Day']!='02-29']
#df_2015['Max_Temp']=df_2015(df_2015[['Data_Value']])

df_2015_tmax=df_2015[df_2015['Element']=='TMAX']
df_2015_tmax=pd.DataFrame(df_2015_tmax.groupby(['Month_Day','Date'])['Data_Value'].max())
df_2015_tmax=pd.merge(df_2015_tmax, df_tmax,  how='right', left_index=True, right_index=True)
df_2015_tmax['GT']=df_2015_tmax['Data_Value_x']>df_2015_tmax['Data_Value_y']
record_high=pd.DataFrame(df_2015_tmax[df_2015_tmax['GT']==1].reset_index())


df_2015_tmin=df_2015[df_2015['Element']=='TMIN']
min_temp=pd.DataFrame(df_2015_tmin.groupby(['Month_Day', 'Date'])['Data_Value'].min())
min_temp=pd.merge(min_temp, df_tmin,  how='right', left_index=True, right_index=True)
min_temp['LT']=min_temp['Data_Value_x']<min_temp['Data_Value_y']
record_low=pd.DataFrame(min_temp[min_temp['LT']==1].reset_index())


#plotting
fig=plt.figure()
observation_dates = np.arange('2015-01-01', '2016-01-01', dtype='datetime64[D]')
plt.plot(observation_dates,df_tmax['Data_Value'], 'c-')
plt.plot(observation_dates,df_tmin['Data_Value'], color="violet")

#Beautiful Graph
ax=plt.gca()
ax.axis(['2015/01/01','2015/12/31',-50,50])

#2015 scatter
plt.scatter(record_high.Date.values,record_high.Data_Value_x.values,  color='navy', s=8)
plt.scatter(record_low.Date.values,record_low.Data_Value_x.values, color='darkviolet', s=8)

#Shading
ax.fill_between(observation_dates, df_tmax['Data_Value'], df_tmin['Data_Value'], facecolor='grey', alpha=0.25)

# Set axis names and title:
plt.xlabel('Date', fontsize=10)
plt.ylabel('° Celsius', fontsize=10)
plt.title('Highs and Lows - Temperature in Ann Arbour, Michigan (2005-2015)', fontsize=12)

# Create legend and title
# loc=0 provides the best position for the legend
plt.legend(['Record high (2005-2014)','Record low (2005-2014)','Record breaking high in 2015','Record breaking low in 2015'],loc=0,frameon=False)

# Where you locate the major and minor ticks:
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15)) 

# What you put at the ticks:
ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))


# rotate the tick labels for the x axis
for item in ax.xaxis.get_ticklabels():
    item.set_rotation(45)



# In[ ]:




# In[ ]:




# In[ ]:




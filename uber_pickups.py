import streamlit as st 
import numpy as np
import pandas as pd 


st.title("Uber pick_ups in New York City")

# Fetching some data

DATE_COLUMN = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)
# DATA_URL = ("uber-raw-data-sep14")


@st.cache
def load_data(nrows):
    data = pd.read_csv( DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis = 'columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

#leting the user know the data is loading 
data_load_state = st.text("data is loading...")

# loading 10,000 data rows into the dataframe
data = load_data(10000)

# notify the user data was succesfully loaded
data_load_state.text("data was successfuly loaded....yaaww!")


# caching the data you don't have to reload the data each time  achange is made 
# @st.cache
# don't use for time varying data i.e live data e.g stock market 


# inspect the raw data
if  st.checkbox('Show Raw data'):
    st.subheader("Raw Data")
    # st.dataframe(data)
    st.write(data)


#Draw a histogram
st.subheader("Number of pickups by hour")

#using numpy to generate a histogram that generates time by the hour 
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

#using streamlit to generate histogram
st.bar_chart(hist_values)


#plot data on the map t
st.subheader("Map of all pickups")
st.map(data)

#show where the concentration of pickups at 17:00 are
hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


#filtering results with a slider, filtering the data in real time 
st.subheader("Using a slider to change the hours") 
hour_to_filter = st.slider('Hour', 0, 23, 17) #min,max and default
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.map(filtered_data)

   





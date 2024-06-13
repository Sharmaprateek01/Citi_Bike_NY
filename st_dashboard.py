################################################ NEW YORK CITI BIKE - 2022 DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title='New York Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Citi Bike currently faces")
st.markdown("Currently, there are concerns about bike availability at certain times, prompting this analysis to investigate the underlying factors and explore potential solutions to enhance distribution efficiency.")

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv')
top20 = pd.read_csv('top20.csv')
df_agg = pd.read_csv('df_agg.csv')

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in Chicago',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)

## Line chart 

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df_agg['date'], y = df_agg['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df_agg['bike_rides_daily'],'color': 'blue'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=df_agg['date'], y = df_agg['avgTemp'], name = 'Daily temperature', marker={'color': df_agg['avgTemp'],'color': 'red'}),
secondary_y=True
)

fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 600
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###

path_to_html = "NY_Trips_Aggregated.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)



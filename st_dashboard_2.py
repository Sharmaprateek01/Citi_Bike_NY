################################################ NEW YORK CITI BIKE - 2022 DASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title='New York Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
                            ["Intro page", "Weather component and bike usage",
                             "Most popular stations",
                             "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data.csv')
top20 = pd.read_csv('top20.csv')
df_agg = pd.read_csv('df_agg.csv')

######################################### DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    st.markdown("The dashboard will help with the expansion problems Citi Bike currently faces")
    st.markdown("Currently, there are concerns about bike availability at certain times, prompting this analysis to investigate the underlying factors and explore potential solutions to enhance distribution efficiency. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("Citi_Bike.png")  # source: http://www.markradcliffe.com/citi-bike-oohdigital
    st.image(myImage)

### Most popular stations page

# Create the season variable

elif page == 'Most popular stations':

    # Create the filter on the side bar

    with st.sidebar:
        season_filter = st.multiselect(label='Select the season', options=df['season'].unique(),
                                       default=df['season'].unique())

    df1 = df.query('season == @season_filter')

    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())
    st.metric(label='Total Bike Rides', value=numerize(total_rides))

    ## Bar chart
    df1['value'] = 1
    df_groupby_bar = df1.groupby('start_station_name', as_index=False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x=top20['start_station_name'], y=top20['value']))

    fig = go.Figure(go.Bar(x=top20['start_station_name'], y=top20['value'], marker={'color': top20['value'], 'colorscale': 'Blues'}))
    fig.update_layout(
        title='Top 20 most popular bike stations in New York',
        xaxis_title='Start stations',
        yaxis_title='Sum of trips',
        width=900, height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart, it is clear that some bike stations in New York City are more popular than others. In the top three, we see W 21 St & 6 Ave, followed by West St and Chambers St, and Broadway & W 58 St. There is a significant difference between the highest and lowest bars on the plot, indicating clear preferences for the leading stations. This is a finding that we could cross-reference with the interactive map, which can be accessed through the sidebar select box.")

elif page == 'Interactive map with aggregated bike trips':

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "NY_Trips_Aggregated.html"

    # Read file and keep in variable
    with open(path_to_html, 'r') as f:
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data, height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("W 21 St & 6 Ave,  West St and Chambers St as well as Broadway & W 58 St. While having the aggregated bike trips filter enabled, we can see that even though W 21 St & 6 Ave is a popular start stations, it doesn't account for the most commonly taken trips.")
    st.markdown("The most common routes are between Vesy PI & River Terrace. E 81 St & York Ave, West Thames St, Murray St & Greenwhich St, E 84 St & 1 Ave, which are predominantly located along the water.")

### Create the dual axis line chart page ###

elif page == 'Weather component and bike usage':

    ## Line chart
    
    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig_2.add_trace(
        go.Scatter(x=df_agg['date'], y=df_agg['bike_rides_daily'], name='Daily bike rides', marker={'color': 'blue'}),
        secondary_y=False
    )

    fig_2.add_trace(
        go.Scatter(x=df_agg['date'], y=df_agg['avgTemp'], name='Daily temperature', marker={'color': 'red'}),
        secondary_y=True
    )

    fig_2.update_layout(
        title='Daily bike trips and temperatures in 2022',
        height=600
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to September.")

elif page == "Recommendations":
    st.header("Conclusions and recommendations")
    bikes = Image.open("Recs_page.png")  # source: DALL-E
    st.image(bikes)
    st.markdown("### Our analysis has shown that Citi Bike should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the water line, such as Vesy PI & River Terrace, Financial District, E 81 St & York Ave, West Thames St, Murray St & Greenwhich St, E 84 St & 1 Ave, Husdson Square and Hudson Yards, Hell's Kitchen, Turtle Bay, Kips Bay, Alphabet City")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs")
    st.markdown("- Create routes that go through & around Central Park. This would be a popular option for tourists and locals alike.")
    st.markdown("- Consider offering more electric bikes, to cater to users with different needs and abilities")
    st.markdown("- Expand the service area into areas that are not well served and are untapped, such as Brooklyn and the Bronx.")
    st.markdown("- Provide information on the routes, such as distance and difficulty. This would allow users to choose a ride that is appropriate for their fitness level and time constraints")
    
    st.markdown("### Some Limitations of the Analysis.")
    st.markdown("The analysis is based on available data, which may not capture all factors affecting bike usage.")
    st.markdown("The recommendations are based on observed trends, which may vary year to year.")
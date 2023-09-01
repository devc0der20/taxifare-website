import streamlit as st
from datetime import datetime
import requests
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium


# streamlit: https://fare-taxifare.streamlit.app/

st.title('Taxi Fare Calculator')
date = st.date_input('Date')
time = st.time_input('Time')

geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)

pickup_location = st.text_input('Enter pickup location')
pickup_point = geolocator.geocode(pickup_location)
pickup_latitude = pickup_point.latitude if pickup_point else None
pickup_longitude = pickup_point.longitude if pickup_point else None

dropoff_location = st.text_input('Enter dropoff location')
dropoff_point = geolocator.geocode(dropoff_location)
dropoff_latitude = dropoff_point.latitude if dropoff_point else None
dropoff_longitude = dropoff_point.longitude if dropoff_point else None

passenger_count = st.selectbox('Passenger Count', [1, 2, 3, 4, 5])

if st.button('Calculate Fare'):
    # Combine the date and time inputs into a single datetime object
    pickup_datetime = datetime.combine(date, time)

    # Calculate the fare using the input data
    params = {
      'pickup_datetime': pickup_datetime.isoformat(),
      'pickup_longitude': pickup_longitude,
      'pickup_latitude': pickup_latitude,
      'dropoff_longitude': dropoff_longitude,
      'dropoff_latitude': dropoff_latitude,
      'passenger_count': passenger_count,
    }

    response = requests.get('https://taxifare.lewagon.ai/predict', params=params)

    # Check if the request was successful
    if response.status_code == 200:
        fare = response.json()['fare']
        st.markdown(f'The estimated fare is <span style="color:green">${fare:.2f}</span>', unsafe_allow_html=True)
    else:
        st.write('An error occurred while calculating the fare.')

    # Create a map centered at the pickup location
    m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=13)

    # Add markers for the pickup and dropoff locations
    folium.Marker([pickup_latitude, pickup_longitude], popup='Pickup').add_to(m)
    folium.Marker([dropoff_latitude, dropoff_longitude], popup='Dropoff').add_to(m)

    # Draw a line between the pickup and dropoff locations
    folium.PolyLine(locations=[(pickup_latitude, pickup_longitude), (dropoff_latitude, dropoff_longitude)], color='red').add_to(m)

    # Display the map
    folium_static(m)

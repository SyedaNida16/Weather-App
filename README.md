import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Page Configuration and Custom CSS for enhanced design
st.set_page_config(page_title="Stunning Weather App", page_icon="🌤️", layout="centered")
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #e0c3fc, #8ec5fc);
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Title and Description
st.title("🌤️ Stunning Weather App")
st.write("Discover the current weather conditions of your favorite city!")

# Dropdown options for city and unit selection
cities = ["New York", "Islamabad", "London", "Tokyo", "Sydney", "Berlin", "Paris", "Dubai"]
selected_city = st.selectbox("Choose a city:", cities)
unit_option = st.selectbox("Select Unit:", ("Metric (°C, m/s)", "Imperial (°F, mph)"))
unit = "metric" if unit_option == "Metric (°C, m/s)" else "imperial"

# OpenWeatherMap API details
API_KEY = "e9505488abb2cfd5e75546f8dc8d8b31"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, units="metric"):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch weather data: {e}")
        return None

if st.button("Get Weather", help="Click to fetch the latest weather data"):
    with st.spinner("Fetching weather data..."):
        weather_data = get_weather(selected_city, unit)
    if weather_data:
        st.success("Weather data fetched successfully!")
        
        # Extract and display city and country information
        city_name = weather_data.get("name", selected_city)
        country = weather_data.get("sys", {}).get("country", "")
        st.header(f"Weather in {city_name}, {country}")
        
        # Extract detailed weather metrics
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"].get("feels_like", temp)
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        wind_speed = weather_data["wind"]["speed"]
        description = weather_data["weather"][0]["description"].title()
        icon = weather_data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        
        # Convert sunrise and sunset times using the timezone offset
        sunrise_epoch = weather_data.get("sys", {}).get("sunrise")
        sunset_epoch = weather_data.get("sys", {}).get("sunset")
        timezone_offset = weather_data.get("timezone", 0)
        def convert_time(epoch):
            local_time = datetime.utcfromtimestamp(epoch + timezone_offset)
            return local_time.strftime('%H:%M:%S')
        sunrise = convert_time(sunrise_epoch) if sunrise_epoch else "N/A"
        sunset = convert_time(sunset_epoch) if sunset_epoch else "N/A"
        
        # Display the weather icon and description side-by-side
        col_icon, col_desc = st.columns([1, 2])
        with col_icon:
            st.image(icon_url)
        with col_desc:
            st.subheader(description)
        
        # Show key metrics in two columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temperature", f"{temp}°{'C' if unit=='metric' else 'F'}")
            st.metric("Feels Like", f"{feels_like}°{'C' if unit=='metric' else 'F'}")
            st.metric("Humidity", f"{humidity}%")
        with col2:
            st.metric("Wind Speed", f"{wind_speed} {'m/s' if unit=='metric' else 'mph'}")
            st.metric("Pressure", f"{pressure} hPa")
            st.metric("Sunrise", sunrise)
            st.metric("Sunset", sunset)
        
        # Display location map using the provided coordinates
        coord = weather_data.get("coord", {})
        if coord:
            st.subheader("Location")
            lat = coord.get("lat")
            lon = coord.get("lon")
            st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))
    else:
        st.error("Could not fetch weather data. Please check the city name or try again later.")

# Footer with credits
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io/) and [OpenWeatherMap](https://openweathermap.org/)")

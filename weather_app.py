import streamlit as st
import requests

# OpenWeatherMap API details
API_KEY = "e9505488abb2cfd5e75546f8dc8d8b31"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """
    Fetch weather data for a given city using the OpenWeatherMap API.
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch weather data: {e}")
        return None

#User Interface (UI)
st.title("🌤️ Weather App")
st.write("Welcome to the Weather App! Select a city below to check its current weather conditions.")

# Cities 
cities = ["New York", "Islamabad", "London", "Tokyo", "Sydney", "Berlin", "Paris", "Dubai"]
selected_city = st.selectbox("Choose a city:", cities, index=0)  

if st.button("Get Weather", help="Click to fetch the latest weather data"):
    with st.spinner("Fetching weather data..."):
        weather_data = get_weather(selected_city)

    if weather_data:
        st.success("Weather data fetched successfully!")
        st.subheader(f"🌍 Weather in {selected_city}")

        # Display weather metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temperature", f"{weather_data['main']['temp']}°C")
            st.metric("Humidity", f"{weather_data['main']['humidity']}%")
        with col2:
            st.metric("Wind Speed", f"{weather_data['wind']['speed']} m/s")
            st.metric("Pressure", f"{weather_data['main']['pressure']} hPa")

        # Weather description
        weather_description = weather_data['weather'][0]['description'].title()
        st.write(f"**Weather Condition:** {weather_description}")

    else:
        st.error("Could not fetch weather data. Please check the city name or try again later.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io/) and [OpenWeatherMap](https://openweathermap.org/)")

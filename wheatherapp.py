import streamlit as st
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO

# -----------------------------
# Config
# -----------------------------
st.set_page_config(
    page_title="🌤 Modern Weather App",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_KEY = "bd86f21f4734ed3d7e5aad81c3720031"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🌤 Weather App")
city = st.sidebar.text_input("Enter City", "London")
units = st.sidebar.selectbox("Units", ["metric", "imperial"])
st.sidebar.markdown("Made with ❤️ by Your Name")

# -----------------------------
# Function to get weather
# -----------------------------
def get_weather(city, units="metric"):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if data.get("cod") != 200:
            return None
        return data
    except Exception as e:
        st.error("Error fetching weather data")
        return None

# -----------------------------
# Weather Background Colors
# -----------------------------
def get_bg_color(weather_main):
    mapping = {
        "Clear": "#FFD966",      # Sunny yellow
        "Clouds": "#A9A9A9",     # Gray clouds
        "Rain": "#76c7f0",       # Blue
        "Drizzle": "#76c7f0",
        "Thunderstorm": "#4B0082", # Dark purple
        "Snow": "#ADD8E6",       # Light blue
        "Mist": "#C0C0C0",       # Silver
        "Fog": "#C0C0C0",
        "Haze": "#C0C0C0",
    }
    return mapping.get(weather_main, "#87CEEB")  # default sky blue

# -----------------------------
# Main Content
# -----------------------------
st.title("🌤 Modern Weather App")

if city:
    data = get_weather(city, units)
    if data:
        weather = data["weather"][0]
        main = weather["main"]
        desc = weather["description"].capitalize()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        icon_code = weather["icon"]

        # Background color
        bg_color = get_bg_color(main)
        st.markdown(f"<div style='background-color:{bg_color}; padding:20px; border-radius:15px'>", unsafe_allow_html=True)

        col1, col2 = st.columns([1,2])
        with col1:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
            response = requests.get(icon_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, use_column_width=True)
        with col2:
            st.markdown(f"### {city}, {data['sys']['country']}")
            st.markdown(f"**{desc}**")
            st.markdown(f"Temperature: **{temp}°{'C' if units=='metric' else 'F'}**")
            st.markdown(f"Feels like: **{feels}°{'C' if units=='metric' else 'F'}**")
            st.markdown(f"Humidity: **{humidity}%**")
            st.markdown(f"Wind: **{wind} m/s**")
            st.markdown(f"Last update: {datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')} UTC")

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("City not found or API error.")



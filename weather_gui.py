import tkinter as tk
from tkinter import messagebox
import requests
import pyttsx3

def get_weather_description(code):
    weather_descriptions = {
        0: "☀️ – ఎండ",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Overcast ☁️",
        45: "Fog 🌫️",
        48: "Rime Fog ❄️🌫️",
        51: "Drizzle 🌦️",
        61: "Rain 🌧️",
        71: "Snow ❄️",
        80: "Rain Showers 🌦️",
        95: "Thunderstorm ⛈️"
    }
    return weather_descriptions.get(code, f"Unknown (code {code})")


def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if "results" in geo_data:
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            location_name = geo_data["results"][0]["name"]

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            current = weather_data["current_weather"]
            temp = current["temperature"]
            wind = current["windspeed"]
            code = current["weathercode"]
            weather_desc = get_weather_description(code)

            result_text = (
                f"📍 City: {location_name}\n"
                f"🌡️ Temperature: {temp}°C\n"
                f"💨 Wind Speed: {wind} km/h\n"
                f"{weather_desc}"
            )
            output_label.config(text=result_text)

            # Speak it out loud
            speak(f"The temperature in {location_name} is {temp} degrees Celsius with wind speed {wind} kilometers per hour. Weather is {weather_desc.split()[0]}.")

        else:
            messagebox.showerror("Error", "City not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# GUI setup
window = tk.Tk()
window.title("Weather App with Voice")
window.geometry("400x300")

label = tk.Label(window, text="Enter City Name:")
label.pack(pady=10)

city_entry = tk.Entry(window, width=30)
city_entry.pack(pady=5)

get_button = tk.Button(window, text="Get Weather", command=get_weather)
get_button.pack(pady=10)

output_label = tk.Label(window, text="", font=("Arial", 12))
output_label.pack(pady=10)

window.mainloop()

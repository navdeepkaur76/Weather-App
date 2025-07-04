import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

def get_weather():
    city = city_entry.get()
    api_key = "03f6d152c684f1bea5891f52499dd692"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    url = f"{base_url}?appid={api_key}&q={city}&units=metric"

    try:
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code != 200 or "message" in weather_data:
            messagebox.showerror("Error", weather_data.get("message", "Failed to retrieve weather."))
            return

        icon_code = weather_data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_img_data = icon_response.content
        icon_image = Image.open(io.BytesIO(icon_img_data))
        icon_photo = ImageTk.PhotoImage(icon_image)

        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        weather_text = f"""
City: {weather_data['name']}
Weather: {weather_data['weather'][0]['description'].capitalize()}
Temperature: {weather_data['main']['temp']} °C
Min Temp: {weather_data['main']['temp_min']} °C
Max Temp: {weather_data['main']['temp_max']} °C
Pressure: {weather_data['main']['pressure']} hPa
Humidity: {weather_data['main']['humidity']}%
Wind Speed: {weather_data['wind']['speed']} m/s
        """
        weather_label.config(text=weather_text.strip())

    except Exception as e:
        messagebox.showerror("Error", str(e))

# UI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("500x400")
root.configure(bg="#add8e6")

# Top Frame for Input
frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')

city_entry = tk.Entry(frame, font=("Courier", 14))
city_entry.place(relwidth=0.65, relheight=1)
city_entry.insert(0, "London")

get_weather_button = tk.Button(frame, text="Get Weather", font=("Courier", 12), command=get_weather)
get_weather_button.place(relx=0.7, relwidth=0.3, relheight=1)

# Display Weather Info
weather_frame = tk.Frame(root, bg='#ffffff', bd=10)
weather_frame.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.6, anchor='n')

weather_label = tk.Label(weather_frame, font=("Courier", 12), justify='left', anchor='nw')
weather_label.place(relwidth=0.75, relheight=1)

# Icon Display
icon_label = tk.Label(weather_frame, bg="#ffffff")
icon_label.place(relx=0.8, rely=0.1, relwidth=0.2, relheight=0.4)

root.mainloop()

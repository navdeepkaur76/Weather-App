import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk

def get_weather():
    city = city_entry.get()
    api_key = "03f6d152c684f1bea5891f52499dd692"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = base_url + "appid=" + api_key + "&q=" + city

    weather_label.config(text="Loading...")
    icon_label.config(image="")
    response = requests.get(url)
    weather_data = response.json()

    if "message" in weather_data:
        messagebox.showerror("Error", weather_data["message"])
    else:
        weather_text = f"City: {city}\n"
        weather_text += f"Temperature: {weather_data['main']['temp']}°F\n"
        weather_text += f"Pressure: {weather_data['main']['pressure']} hPa\n"
        weather_text += f"Humidity: {weather_data['main']['humidity']}%\n"
        weather_text += f"Min Temp: {weather_data['main']['temp_min']}°F\n"
        weather_text += f"Max Temp: {weather_data['main']['temp_max']}°F\n"
        weather_text += f"Wind Speed: {weather_data['wind']['speed']} m/s\n"
        weather_text += f"Description: {weather_data['weather'][0]['description']}\n"
        weather_text += f"Sunrise: {weather_data['sys']['sunrise']}\n"
        weather_text += f"Sunset: {weather_data['sys']['sunset']}\n"
        weather_label.config(text=weather_text)

        icon_name = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_name}@2x.png"
        icon_data = requests.get(icon_url)

        with open("icon.png", "wb") as f:
            f.write(icon_data.content)
        icon_image = ImageTk.PhotoImage(Image.open("icon.png"))
        icon_label.config(image=icon_image)
        icon_label.image = icon_image

root = tk.Tk()
root.title("Weather App")

# Create a default solid color instead of gradient to prevent errors
root.configure(bg="#8EC5FC")

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

city_entry = tk.Entry(frame, font=("Courier", 14))
city_entry.place(relwidth=0.65, relheight=1)
city_entry.insert(0, "Washington D.C.")

get_weather_button = tk.Button(frame, text="Get Weather", font=("Courier", 12), command=get_weather)
get_weather_button.place(relx=0.7, relwidth=0.3, relheight=1)

weather_frame = tk.Frame(root, bg='#80c1ff', bd=10)
weather_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.5, anchor='n')

weather_label = tk.Label(weather_frame, font=("Courier", 14), justify='left', bd=5, bg='#80c1ff')
weather_label.place(relwidth=1, relheight=1)

icon_frame = tk.Frame(weather_frame, bg='#80c1ff')
icon_label = tk.Label(icon_frame, bg='#80c1ff')
icon_label.place(relx=0.5, rely=0.5, anchor='center')
icon_frame.place(relx=0.8, rely=0.3, relwidth=0.2, relheight=0.4, anchor='n')

root.mainloop()

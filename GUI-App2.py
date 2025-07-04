from tkinter import *
import requests
import json
import datetime
from PIL import ImageTk, Image

# Create main application window
root = Tk()
root.title("Weather App")
root.geometry("450x700")
root.configure(bg="white")

# Logo
logo_img = ImageTk.PhotoImage(Image.open("logo.png"))
logo_label = Label(root, image=logo_img, bg="white")
logo_label.place(x=0, y=520)

# Date and Time
now = datetime.datetime.now()
day_label = Label(root, text=now.strftime('%A'), bg='white', font=("bold", 15))
day_label.place(x=5, y=130)

date_label = Label(root, text=now.strftime('%d %B %Y'), bg='white', font=("bold", 15))
date_label.place(x=100, y=130)

time_label = Label(root, text=now.strftime('%I:%M %p'), bg='white', font=("bold", 15))
time_label.place(x=10, y=160)

# Day/Night Image Logic (uses 24-hour format)
current_hour = now.hour
if 6 <= current_hour < 18:
    weather_icon = ImageTk.PhotoImage(Image.open('sun.png'))
else:
    weather_icon = ImageTk.PhotoImage(Image.open('moon.png'))

icon_label = Label(root, image=weather_icon, bg="white")
icon_label.place(x=210, y=200)

# City Entry
city_var = StringVar()
city_entry = Entry(root, textvariable=city_var, width=45)
city_entry.grid(row=1, column=0, ipady=10, sticky=W+E+N+S)

# Weather Fetch Function
def fetch_weather():
    api_key = "03f6d152c684f1bea5891f52499dd692"
    city = city_var.get()
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        )
        data = json.loads(response.content)

        # Extract info
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        lon = data['coord']['lon']
        lat = data['coord']['lat']
        country = data['sys']['country']
        city_name = data['name']

        # Update UI
        lt.config(text=f"{temp:.1f}°")
        label_humidity.config(text=f"{humidity}%")
        max_temp.config(text=f"{temp_max}°")
        min_temp.config(text=f"{temp_min}°")
        label_lon.config(text=f"{lon}")
        label_lat.config(text=f"{lat}")
        label_country.config(text=country)
        label_citi.config(text=city_name)

    except Exception as e:
        lt.config(text="N/A")
        label_citi.config(text="Error")
        label_country.config(text="")
        label_lon.config(text="")
        label_lat.config(text="")
        label_humidity.config(text="")
        max_temp.config(text="")
        min_temp.config(text="")

# Search Button
search_button = Button(root, text="Search", command=fetch_weather)
search_button.grid(row=1, column=1, padx=5, sticky=W+E+N+S)

# Weather Information Labels
label_citi = Label(root, text="...", bg='white', font=("bold", 15))
label_citi.place(x=10, y=63)

label_country = Label(root, text="...", bg='white', font=("bold", 15))
label_country.place(x=135, y=63)

label_lon = Label(root, text="...", bg='white', font=("Helvetica", 15))
label_lon.place(x=25, y=95)

label_lat = Label(root, text="...", bg='white', font=("Helvetica", 15))
label_lat.place(x=95, y=95)

lt = Label(root, text="...", bg='white', font=("Helvetica", 110), fg='black')
lt.place(x=18, y=220)

# Temperature and Humidity
Label(root, text="Humidity:", bg='white', font=("bold", 15)).place(x=3, y=400)
label_humidity = Label(root, text="...", bg='white', font=("bold", 15))
label_humidity.place(x=107, y=400)

Label(root, text="Max. Temp.:", bg='white', font=("bold", 15)).place(x=3, y=430)
max_temp = Label(root, text="...", bg='white', font=("bold", 15))
max_temp.place(x=128, y=430)

Label(root, text="Min. Temp.:", bg='white', font=("bold", 15)).place(x=3, y=460)
min_temp = Label(root, text="...", bg='white', font=("bold", 15))
min_temp.place(x=128, y=460)

note = Label(root, text="All temperatures in °C", bg='white', font=("italic", 10))
note.place(x=95, y=495)

root.mainloop()

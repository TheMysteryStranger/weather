import os
import sys
import requests
from tkinter import *
from PIL import Image, ImageTk
from tkinter.messagebox import showerror


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def save_image(url):
    response = requests.get(url)
    with open(resource_path("weather_icon.png"), "wb") as file:
        file.write(response.content)
    image = Image.open(resource_path("weather_icon.png"))
    return ImageTk.PhotoImage(image)


def show_weather():
    city_name = weather_entry.get()
    if not city_name:
        weather_info.config(text="")
        picture.config(image="", background="#F0F0F0")
        showerror("Ошибка", "Строка не может быть пустой!")
    else:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}"
                                f"&appid=c5090954db2c4c879646020b93d20565&lang=ru")
        if response.status_code != 404:
            response = response.json()
            img = save_image(f"https://openweathermap.org/img/wn/{response['weather'][0]['icon']}@2x.png")
            picture.config(image=img, background="cyan")
            picture.image = img
            weather_info.config(text=f"{(response['weather'][0]['description']).capitalize()}\n"
                                     f"Температура: {round(response['main']['temp'] - 273.15)}\n"
                                     f"Скорость ветра: {response['wind']['speed']} м/с")
        else:
            weather_info.config(text="")
            picture.config(image="", background="#F0F0F0")
            showerror("Ошибка", "Указанный город не найден в OpenWeatherMap!")


window = Tk()
window.geometry("500x500")
window.title("Прогноз погоды")
window.resizable(False, False)

welcome_text = Label(window, text="Прогноз погоды", font=("Times New Roman", 40, "bold"))
welcome_text.pack()

weather_entry = Entry(window)
weather_entry.pack()
weather_entry.focus()

btn = Button(window, text="Показать погоду", command=show_weather)
btn.pack(pady=10)

picture = Label(window)
picture.pack()

weather_info = Label(window, font=("Times New Roman", 30))
weather_info.pack()

window.mainloop()

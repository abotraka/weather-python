import tkinter as tk
from tkinter import messagebox
import requests

# OpenWeatherMap API key
api_key = '4c2be1eedda3d0701421de9dc6d8a1fa'
weather_url = "http://api.openweathermap.org/data/2.5/weather"

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App by ahmed rabea")
        self.geometry("400x550")
        self.configure(bg="#f0f0f0")

        tk.Label(self, text="Enter city name:", font=('Helvetica', 14), bg="#f0f0f0").pack(pady=10)

        self.city_entry = tk.Entry(self, width=30, font=('Helvetica', 14))
        self.city_entry.pack(pady=5)
        self.city_entry.bind("<KeyRelease>", self.search_city)

        self.cities_listbox = tk.Listbox(self, selectmode="single", font=('Helvetica', 12))
        self.cities_listbox.pack(pady=5)
        self.cities_listbox.bind("<Double-Button-1>", self.select_city)
        self.cities_list = ["Cairo", "Alexandria", "Giza", "Shubra El Kheima", "Port Said", "Suez", "Luxor", "Asyut", "Ismailia", "Fayyum"]

        get_weather_button = tk.Button(self, text="Get Weather", command=self.get_weather, font=('Helvetica', 14), bg="#4caf50", fg="white", relief="flat", activebackground="#43a047")
        get_weather_button.pack(pady=10)

        self.result_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.result_frame.grid_columnconfigure(0, weight=1)

        self.result_label = tk.Label(self.result_frame, text="", justify='left', font=('Helvetica', 12), bg="#ffffff")
        self.result_label.grid(row=0, column=0, sticky="nsew")

    def search_city(self, event=None):
        search_term = self.city_entry.get().lower()
        self.cities_listbox.delete(0, tk.END)
        for city in self.cities_list:
            if search_term in city.lower():
                self.cities_listbox.insert(tk.END, city)

    def select_city(self, event=None):
        selected_index = self.cities_listbox.curselection()
        if selected_index:
            selected_city = self.cities_list[int(selected_index[0])]
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, selected_city)

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Input Error", "Please enter a city name")
            return

        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',
            'lang': 'en'
        }
        response = requests.get(weather_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']
            rain = data.get('rain', {}).get('1h', 0)

            result_text = (f"Weather in {city}:\n"
                           f"Description: {weather}\n"
                           f"Temperature: {temp}°C\n"
                           f"Humidity: {humidity}%\n"
                           f"Wind Speed: {wind_speed} m/s\n"
                           f"Pressure: {pressure} hPa\n"
                           f"Rainfall Chance: {rain} mm")
            self.result_label.config(text=result_text)
        else:
            messagebox.showerror("API Error", "Could not retrieve weather data. Please check the city name and API key.")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()

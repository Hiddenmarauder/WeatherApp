import tkinter as tk
import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def get_weather():
    try:
        city = entry_city.get()
        api_key = 'bb4f0f098bb7f4f9fc55cfed71442650'  # Replace with your actual API key

        # Make an API request to retrieve weather data
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            weather_info = data['weather'][0]['description']
            temperature = data['main']['temp']
            temperature = round(temperature - 273.15, 2)  # Convert temperature to Celsius
            humidity = data['main']['humidity']

            weather_label['text'] = f"Weather: {weather_info}"
            temperature_label['text'] = f"Temperature: {temperature} °C"
            humidity_label['text'] = f"Humidity: {humidity}%"
        else:
            weather_label['text'] = "Error: Invalid city"
    except EOFError:
        weather_label['text'] = "Error: Ran out of input"

def autocomplete(event):
    entered_text = entry_city.get()
    if entered_text:
        matching_cities = [city for city in city_list if city.lower().startswith(entered_text.lower())]
        autocomplete_listbox.delete(0, tk.END)
        for city in matching_cities:
            autocomplete_listbox.insert(tk.END, city)
        autocomplete_listbox.place(x=entry_city.winfo_x(), y=entry_city.winfo_y() + entry_city.winfo_height())
    else:
        autocomplete_listbox.place_forget()

def on_select(event):
    selected_city = autocomplete_listbox.get(tk.ACTIVE)
    entry_city.delete(0, tk.END)
    entry_city.insert(tk.END, selected_city)
    autocomplete_listbox.place_forget()

def on_focus_out(event):
    autocomplete_listbox.place_forget()

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Create and pack the city entry
entry_city = tk.Entry(root)
entry_city.pack()

# Create and pack the Get Weather button
btn_get_weather = tk.Button(root, text="Get Weather", command=get_weather)
btn_get_weather.pack()

# Create and pack labels to display weather information
weather_label = tk.Label(root, text="Weather: ")
weather_label.pack()

temperature_label = tk.Label(root, text="Temperature: ")
temperature_label.pack()

humidity_label = tk.Label(root, text="Humidity: ")
humidity_label.pack()

# City list for auto-completion
city_list = ['New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'Rome', 'Berlin']

# Create autocomplete listbox
autocomplete_listbox = tk.Listbox(root, width=entry_city.winfo_width())
autocomplete_listbox.bind('<<ListboxSelect>>', on_select)
autocomplete_listbox.bind('<FocusOut>', on_focus_out)

entry_city.bind('<KeyRelease>', autocomplete)

if __name__ == '__main__':
    app.run(debug=True)

root.mainloop()


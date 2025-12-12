import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv("WEATHER_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error = None

    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            if not API_KEY:
                error = "API key is not set. Please set WEATHER_API_KEY environment variable."
            else:
                try:
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
                    response = requests.get(url, timeout=5)
                    response.raise_for_status()
                    data = response.json()

                    weather_data = {
                        'city': data['name'],
                        'temperature': data['main']['temp'],
                        'condition': data['weather'][0]['description'].title(),
                        'humidity': data['main']['humidity'],
                        'windspeed': data['wind']['speed']
                    }

                except requests.exceptions.Timeout:
                    error = "Request timed out. Please try again."
                except requests.exceptions.ConnectionError:
                    error = "Could not connect to the weather service. Check your internet."
                except requests.exceptions.HTTPError:
                    error = "Could not fetch weather data. Check the city name."
                except Exception as e:
                    error = f"An unexpected error occurred: {str(e)}"

    return render_template('index.html', weather=weather_data, error=error)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


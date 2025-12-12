import requests
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error = None
    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            try:
                url = f"https://wttr.in/{location}?format=j1"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    current = data['current_condition'][0]
                    weather_data = {
                            'city': location,
                            'temperature': current['temp_C'],
                            'condition': current['weatherDesc'][0]['value'],
                            'humidity': current['humidity'],
                            'windspeed': current['windspeedKmph']
                            }
                else:
                    error = "Could not fetch weather data."
            except Exception as e:
                error = f"Error: {str(e)}"
        return render_template('index.html', weather=weather_data, error=error)
if __name__ == '__main__':
    app.run(host="192.168.1.29", port=5000, debug=True)
                

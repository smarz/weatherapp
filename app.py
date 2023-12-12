#!/usr/bin/env python3
import requests
from datetime import datetime, date
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'Weather.sqlite3')

db = SQLAlchemy(app)

# Adding the Promethius metric
metrics = PrometheusMetrics(app)

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(20))
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

def get_temperature(city):
    api_key = "0259947fdd56379a2312929e7e8db0d5"
    units = "metric"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print(f"API Request Failed. Status Code: {response.status_code}")
        print(f"Error Message: {data.get('message', 'No error message available')}")
        return None, None, None

    print(f"API Response for {city}: {data}")

    temperature = data.get("main", {}).get("temp")
    dt = data.get("dt")
    date_time = datetime.utcfromtimestamp(dt)
    description = data.get("weather", [{}])[0].get("description")
    icon = data.get("weather", [{}])[0].get("icon")
    country = data.get("sys", {}).get("country")
    lat = data.get("coord", {}).get("lat")
    lon = data.get("coord", {}).get("lon")

    return temperature, date_time, description, icon, country, lat, lon

@app.route('/', methods=['GET', 'POST'])
@metrics.do_not_track()
def display_temperature():
    selected_city = request.form.get('city')

    current_temperature = get_temperature(selected_city) if selected_city else None

    if selected_city and current_temperature[0] is not None:
        temperature, date_time, description, icon, country, lat, lon = current_temperature
        new_entry = Weather(date_time=date_time, temperature=temperature, city=selected_city, description=description, icon=icon, country=country, lat=lat, lon=lon)
        db.session.add(new_entry)
        db.session.commit()

    # Fetch the 20 latest entries
    weather_entries = Weather.query.order_by(Weather.date_time.desc()).limit(20).all()

    return render_template('index.html', temperature=current_temperature, selected_city=selected_city, weather_entries=weather_entries)

@app.route('/average_temp/', methods=['GET'])
@metrics.do_not_track()
def average_temp():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Convert datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        query = Weather.query.filter(Weather.date_time.between(start_date, end_date))

        count = query.count()
        total_temp = sum(entry.temperature for entry in query)
        average_temp = total_temp / count if count > 0 else 0.0

        # Fetch the 20 latest entries
        weather_entries = Weather.query.order_by(Weather.date_time.desc()).limit(20).all()

        return render_template('index.html', average_temp=average_temp, start_date=start_date, end_date=end_date, weather_entries=weather_entries)

    except Exception as e:
        return f"Error: {str(e)}"


# CLI command to create the database
@app.cli.command("create_db")
def create_db():
    db.create_all()
    print("Database created successfully.")


if __name__ == "__main__":
    app.run(debug=False)

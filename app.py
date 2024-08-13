from flask import Flask, render_template, request, jsonify
import numpy as np
import json
import os
from geopy.geocoders import Nominatim

app = Flask(__name__, static_url_path='/static')
# Global variables to hold filtered data
gyro_data_raw = []
gyro_data_filtered = []
accel_data_raw = []
accel_data_filtered = []
WINDOW_SIZE = 4

# def update_and_filter(new_gyro, new_accel):
#     # Append new raw data
#     gyro_data_raw.append(new_gyro)
#     accel_data_raw.append(new_accel)
#
#     # Keep only the last WINDOW_SIZE elements
#     if len(gyro_data_raw) > WINDOW_SIZE:
#         gyro_data_raw.pop(0)
#     if len(accel_data_raw) > WINDOW_SIZE:
#         accel_data_raw.pop(0)
#
#     # Apply moving average filter
#     filtered_gyro = np.mean(gyro_data_raw, axis=0)
#     filtered_accel = np.mean(accel_data_raw, axis=0)
#
#     # Store filtered data
#     gyro_data_filtered.append(filtered_gyro)
#     accel_data_filtered.append(filtered_accel)
#
#     if len(gyro_data_filtered) > 2:
#         # Calculate delta (dynamic change) between the last two filtered samples
#         delta_gyro = gyro_data_filtered[-1] - gyro_data_filtered[-2]
#         delta_accel = accel_data_filtered[-1] - accel_data_filtered[-2]
#     else:
#         delta_gyro = np.zeros(3)
#         delta_accel = np.zeros(3)
#
#     return filtered_gyro, filtered_accel, delta_gyro, delta_accel

def get_lat_long(location_name):
    geolocator = Nominatim(user_agent="geopy_example", timeout=10)
    location = geolocator.geocode(location_name)

    if location:
        latitude, longitude = location.latitude, location.longitude
        return latitude, longitude
    else:
        return None

@app.route('/')
def index():
    return render_template('updatedmap.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/googlemap')
def googlemap():
    return render_template('googlemap.html')

@app.route('/updatedmap')
def updatedmap():
    return render_template('updatedmap.html')

@app.route('/fetch')
def fetch():
    return render_template('fetch.html')

@app.route('/sensor-data', methods=['POST'])
def receive_data():
    # data = request.json
    latitude = None
    longitude = None

    # Extract data from the POST request
    data = request.form

    # Log the received data to the console
    print("Received data:")
    print(f"Accel X: {data.get('ax')}")
    print(f"Accel Y: {data.get('ay')}")
    print(f"Accel Z: {data.get('az')}")
    print(f"Gyro X: {data.get('gx')}")
    print(f"Gyro Y: {data.get('gy')}")
    print(f"Gyro Z: {data.get('gz')}")

    if data.get('latitude') and data.get('longitude'):
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        print(f"Latitude: {latitude}")

    if data.get('longitude') == "0.000000":
        location_name = "Str. Visan 82"
        result = get_lat_long(location_name)
        if result:
            latitude, longitude = result

# Print the final longitude value after any adjustments
    print(f"Longitude: {longitude}")

# # Respond back to the ESP32
#     return jsonify({"status": "success"}), 200

    gps_data = {
        "latitude": latitude,
        "longitude": longitude
    }

    json_file_path = 'templates/gps.json'

    # Append new data to the JSON file
    # if os.path.exists(json_file_path):
    #     # Read existing data
    #     with open(json_file_path, 'r') as json_file:
    #         try:
    #             data_list = json.load(json_file)
    #         except json.JSONDecodeError:
    #             data_list = []
    # else:
    #     # Create a new file if it doesn't exist
    #     data_list = []
    #
    # # Append the new GPS data
    # data_list.update(gps_data)

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(gps_data, json_file, indent=4)

    # Send back a JSON response with the data
    return jsonify({
        "status": "success",
        "latitude": latitude,
        "longitude": longitude,
    })

    # with open('data/gps-data.json', 'w') as json_file:
    #     json.dump(gps_data, json_file)
    #
    # # Send back a JSON response with the data
    # return jsonify({
    #     "status": "success",
    #     "latitude": latitude,
    #     "longitude": longitude,
    # })
    #
    # with open('data/gps-data.json', 'r') as json_file:
    #     json.load(json_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

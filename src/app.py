from flask import Flask, jsonify, request , abort
from flask_swagger_ui import get_swaggerui_blueprint
import json
import os


# Define the list of IP addresses to reject
blocked_ips = ["192.168.0.101"]

# Decorator to check if the request IP is in the blocked_ips list
def block_ip(func):
    def wrapper(*args, **kwargs):
        if request.remote_addr in blocked_ips:
            # If the request IP is in the blocked_ips list, return a 403 Forbidden response
            return abort(403)
        return func(*args, **kwargs)
    return wrapper

app = Flask(__name__)

# Define a route for the Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Application Server"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# File path for the local document file
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# Define CRUD operations

# Read operation - Retrieve all data from the document file
def read_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Create operation - Add new data to the document file
def create_data(new_data):
    all_data = read_data()
    all_data.append(new_data)
    with open(DATA_FILE, 'w') as file:
        json.dump(all_data, file, indent=4)

# Update operation - Update existing data in the document file
def update_data(updated_data):
    all_data = read_data()
    for index, data in enumerate(all_data):
        if data['id'] == updated_data['id']:
            all_data[index] = updated_data
            break
    with open(DATA_FILE, 'w') as file:
        json.dump(all_data, file, indent=4)

# Delete operation - Remove data from the document file
def delete_data(id):
    all_data = read_data()
    all_data = [data for data in all_data if data['id'] != id]
    with open(DATA_FILE, 'w') as file:
        json.dump(all_data, file, indent=4)

# Define your API routes

@app.route('/get/data')
def get_all_data():
    """Retrieve all data."""
    return jsonify(read_data())

@app.route('/get/data/<int:data_id>')
def get_data(data_id):
    """Retrieve data by ID."""
    all_data = read_data()
    for data in all_data:
        if data['id'] == data_id:
            return jsonify(data)
    return jsonify({'message': 'Data not found'})

@app.route('/add/data', methods=['POST'])
def add_data():
    """Add new data."""
    new_data = request.json
    create_data(new_data)
    return jsonify({'message': 'Data added successfully'})

@app.route('/update/data/<int:data_id>', methods=['PUT'])
def update_data_route(data_id):
    """Update data by ID."""
    updated_data = request.json
    updated_data['id'] = data_id
    update_data(updated_data)
    return jsonify({'message': 'Data updated successfully'})

@app.route('/delete/data/<int:data_id>', methods=['DELETE'])
@block_ip
def delete_data_route(data_id):
    """Delete data by ID."""
    delete_data(data_id)
    return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

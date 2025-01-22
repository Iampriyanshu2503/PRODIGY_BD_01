from flask import Flask, jsonify, request
import uuid
import re

app = Flask(__name__)

# In-memory storage (hashmap)
users = {}

# Validate email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Create a user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Basic input validation
    if not data or 'name' not in data or 'email' not in data or 'age' not in data:
        return jsonify({'error': 'Missing fields'}), 400
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email'}), 400
    if not isinstance(data['age'], int) or data['age'] <= 0:
        return jsonify({'error': 'Age must be a positive integer'}), 400
    
    # Create user
    user_id = str(uuid.uuid4())
    users[user_id] = {
        'id': user_id,
        'name': data['name'],
        'email': data['email'],
        'age': data['age']
    }
    return jsonify(users[user_id]), 201

# Read a user
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

# Update a user
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        if not is_valid_email(data['email']):
            return jsonify({'error': 'Invalid email'}), 400
        user['email'] = data['email']
    if 'age' in data:
        if not isinstance(data['age'], int) or data['age'] <= 0:
            return jsonify({'error': 'Age must be a positive integer'}), 400
        user['age'] = data['age']
    
    users[user_id] = user
    return jsonify(user), 200

# Delete a user
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    del users[user_id]
    return jsonify({'message': 'User deleted successfully'}), 200

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(list(users.values())), 200

if __name__ == '__main__':
    app.run(debug=True)

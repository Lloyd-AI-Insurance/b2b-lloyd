from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import traceback

app = Flask(__name__)
CORS(app, resources={r"/submitForm": {"origins": "http://localhost:5173"}})

@app.route('/submitForm', methods=['POST'])
def handle_form():
    try:
        # Extract data from the received JSON
        data = request.json
        agency_name = data.get('agencyName')
        call_type = data.get('callType')

        # Ensure mandatory data is present
        if not agency_name or not call_type:
            return jsonify({'status': 'error', 'message': 'Missing agency name or call type'}), 400

        # Define headers for the bland API
        headers = {
            'Authorization': 'sk-ekcrk8eijv40synyetthqpkfr97jyk1rk660ai6jx17cp4f8h2klyibc5rwio2ac69',
            'Content-Type': 'application/json'  # Explicitly setting Content-Type
        }

        # Update the data payload with dynamic content
        bland_data = {
            "phone_number": "+16467059086",  # Example phone number
            "from": None,  # To match your curl request during testing
            "task": call_type,
            "model": "enhanced",
            "language": "eng",
            "voice": "maya",
            "voice_settings": {},
            "local_dialing": False,
            "max_duration": 12,
            "answered_by_enabled": False,
            "wait_for_greeting": False,
            "record": False,
            "amd": False,
            "interruption_threshold": 100,
            "temperature": None,
            "transfer_list": {},
            "metadata": {"agencyName": agency_name},
            "pronunciation_guide": [],
            "start_time": None,
            "request_data": {},
            "tools": [],
            "webhook": None
        }

        response = requests.post('https://api.bland.ai/v1/calls', json=bland_data, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad requests
        return jsonify({'status': 'success', 'data': response.json()})

    except requests.exceptions.HTTPError as http_err:
        # Capture HTTP errors from the Bland API response
        return jsonify({'status': 'error', 'message': str(http_err), 'details': response.text}), response.status_code

    except Exception as e:
        traceback.print_exc()  # Print stack trace for debugging
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

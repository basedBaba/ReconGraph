from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import socket
import re
from attack.ipapi import ipapi
from attack.talos import talos
from attack.threatfox import threatfox
from attack.tor import tor
from attack.tranco import tranco
from osint.internetdb import internetdb
from osint.xposedornot import checkEmail
from osint.phone import validate_phone_number
from osint.username import sagemode_wrapper
from file.capa import capa
import tempfile
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groclake.modellake import ModelLake
from dotenv import load_dotenv

load_dotenv()

GROCLAKE_API_KEY = os.getenv('GROCLAKE_API_KEY')
GROCLAKE_ACCOUNT_ID = os.getenv('GROCLAKE_ACCOUNT_ID')

# Initialize ModelLake instance
model_lake = ModelLake()

# Initialize conversation history
conversation_history = [
    {
        "role": "system", 
        "content": """You are a cybersecurity expert assistant specializing in:
        1. Attack surface monitoring and reduction
        2. Digital footprint analysis and protection
        3. File malware analysis and security
        4. Data privacy and protection strategies
        5. Organizational security best practices

        Provide practical, actionable advice while explaining security concepts in an accessible way.
        Focus on helping users understand and implement security measures for their organization.
        When discussing threats or vulnerabilities, always provide mitigation strategies.
        """
    }
]
app = Flask(__name__)
CORS(app, supports_credentials=True) 

IP_REGEX = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
URL_REGEX = r'^([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^\+?[0-9]\d{1,14}$' 


# ipapi -> ipinfo
# talos -> blacklisted ip

@app.route('/')
def home():
    return "Welcome to the ReconGraph"

@app.route('/scan', methods=['POST'])
def scan():
    # Get the input query from the request body
    body = request.get_json()
    ip_or_domain = body.get('query')

    if not ip_or_domain:
        return jsonify({"error": "No IP or domain provided."}), 400

    if re.match(IP_REGEX, ip_or_domain):
        input_type = 'ip'
        ip_to_scan = ip_or_domain
        url_to_scan = None
    elif re.match(URL_REGEX, ip_or_domain):
        input_type = 'domain'
        try:
            ip_to_scan = socket.gethostbyname(ip_or_domain)  # Resolve domain to IP
            url_to_scan = ip_or_domain  # Keep the URL as it is
        except socket.gaierror:
            return jsonify({"error": f"Unable to resolve domain: {ip_or_domain}"}), 400
    else:
        return jsonify({"error": "Invalid IP or domain format."}), 400
    results = {}

    if ip_to_scan:
        results["ipapi"] = ipapi(ip_to_scan)
        results["talos"] = talos(ip_to_scan)
        results["tor"] = tor(ip_to_scan)
        results["internetdb"] = internetdb(ip_to_scan)

    if url_to_scan:
        results["tranco"] = tranco(url_to_scan) 
        results["threatfox"] = threatfox(url_to_scan) 

    return jsonify(results)

@app.route('/footprint', methods=['POST'])
def footprint():
    body = request.get_json()
    query = body.get('query')

    if not query:
        return jsonify({"error": "No IP or domain provided."}), 400
    
    if re.match(EMAIL_REGEX, query):
        input_type = 'email'
        email_to_scan = query
    elif re.match(PHONE_REGEX, query):
        input_type = 'phone'
        phone_to_scan = query
    else:
        username_to_scan = query

    results = {}

    if 'email_to_scan' in locals():
        results["email_scan"] = checkEmail(email_to_scan)  # Replace with your email scan function

    if 'phone_to_scan' in locals():
        results["phone_scan"] = validate_phone_number(phone_to_scan)  # Replace with your phone scan function

    if 'username_to_scan' in locals():
        results["username_scan"] = sagemode_wrapper(username_to_scan)  # Replace with your username scan function

    return jsonify(results)


@app.route("/capa_analyze", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    print(file)

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name
        print(temp_file_path)

        capa_results = capa(temp_file_path)

        return capa_results
    
@app.route('/chat', methods=['POST'])
def chat():
    """Simple chat endpoint"""
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Add user message to history
    conversation_history.append({"role": "user", "content": user_message})
    
    try:
        # Get response from model
        payload = {"messages": conversation_history}
        response = model_lake.chat_complete(payload)
        bot_reply = response.get("answer", "I'm sorry, I couldn't process that. Please try again.")
        
        # Add bot response to history
        conversation_history.append({"role": "assistant", "content": bot_reply})
        
        return jsonify({'response': bot_reply})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

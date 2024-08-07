import os
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_strings_from_heapdump(heap_dump_file):
    try:
        with open(heap_dump_file, 'rb') as file:
            data = file.read()
        # Extract printable strings
        strings = re.findall(b"[ -~]{4,}", data)  # Extract strings of at least 4 printable characters
        return b'\n'.join(strings).decode('utf-8', errors='ignore')
    except Exception as e:
        raise RuntimeError(f"Error extracting strings: {e}")

def search_password_values(strings_output):
    password_values = set()  # Use a set to store unique username-password pairs
    pattern = re.compile(r'"password"\s*:\s*"([^"]+)"', re.IGNORECASE)
    for line in strings_output.splitlines():
        matches = pattern.findall(line)
        for match in matches:
            username_pattern = re.search(r'"username"\s*:\s*"([^"]+)"', line, re.IGNORECASE)
            username = username_pattern.group(1) if username_pattern else "Unknown Username"
            password_values.add((username, match))  # Add as a tuple to the set
    return password_values

def search_client_ids(strings_output):
    client_info = []  # Use a list to store client ID entries
    client_id_pattern = re.compile(r'client_id\s*=\s*([a-z0-9-]+)', re.IGNORECASE)
    redirect_uri_pattern = re.compile(r'redirect_uri\s*=\s*([^&\s]+)', re.IGNORECASE)  # Adjusted regex to match URIs correctly
    client_secret_pattern = re.compile(r'client_secret\s*=\s*([^&\s]+)', re.IGNORECASE)
    username_pattern = re.compile(r'username\s*=\s*([^&\s]+)', re.IGNORECASE)
    password_pattern = re.compile(r'password\s*=\s*([^&\s]+)', re.IGNORECASE)
    user_id_pattern = re.compile(r'userId\s*=\s*([^&\s]+)', re.IGNORECASE)
    
    lines = strings_output.splitlines()
    
    for i, line in enumerate(lines):
        client_id_match = client_id_pattern.search(line)
        if client_id_match:
            client_id = client_id_match.group(1)
            redirect_uris = []

            # Search for redirect_uris in subsequent lines until a different keyword is found
            for j in range(i + 1, len(lines)):
                uri_match = redirect_uri_pattern.search(lines[j])
                if uri_match:
                    redirect_uris.append(uri_match.group(1))
                # Stop if another 'client_id' is found or end of lines
                if client_id_pattern.search(lines[j]):
                    break

            user_id_match = user_id_pattern.search(line)
            if user_id_match:
                user_id = user_id_match.group(1)
                client_info.append({
                    "client_id": client_id,
                    "user_id": user_id
                })
            elif not redirect_uris:  # If no redirect_uris and no user_id found, search for client_secret, username, and password
                client_secret_match = client_secret_pattern.search(line)
                username_match = username_pattern.search(line)
                password_match = password_pattern.search(line)

                client_secret = client_secret_match.group(1) if client_secret_match else "Unknown Client Secret"
                username = username_match.group(1) if username_match else "Unknown Username"
                password = password_match.group(1) if password_match else "Unknown Password"

                client_info.append({
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "username": username,
                    "password": password
                })
            else:
                client_info.append({
                    "client_id": client_id,
                    "redirect_uris": redirect_uris
                })

    return client_info  # Return the list of dictionaries



def search_api_password(strings_output):
    api_password_values = set()  # Use a set to store unique API credentials
    api_password_pattern = re.compile(r'"api\.password"\s*:\s*"([^"]+)"', re.IGNORECASE)
    api_username_pattern = re.compile(r'"api\.username"\s*:\s*"([^"]+)"', re.IGNORECASE)
    api_client_secret_pattern = re.compile(r'"api\.client_secret"\s*:\s*"([^"]+)"', re.IGNORECASE)
    api_base_url_pattern = re.compile(r'"api\.base-url"\s*:\s*"([^"]+)"', re.IGNORECASE)
    api_client_id_pattern = re.compile(r'"api\.client_id"\s*:\s*"([^"]+)"', re.IGNORECASE)

    for line in strings_output.splitlines(): 
        api_password_matches = api_password_pattern.findall(line)
        api_username_matches = api_username_pattern.findall(line)
        api_client_secret_matches = api_client_secret_pattern.findall(line)
        api_base_url_matches = api_base_url_pattern.findall(line)
        api_client_id_matches = api_client_id_pattern.findall(line)

        for api_password in api_password_matches:
            api_username = api_username_matches[0] if api_username_matches else "Unknown API Username"
            api_client_secret = api_client_secret_matches[0] if api_client_secret_matches else "Unknown Client Secret"
            api_base_url = api_base_url_matches[0] if api_base_url_matches else "Unknown Base URL"
            api_client_id = api_client_id_matches[0] if api_client_id_matches else "Unknown Client ID"
            api_password_values.add((api_username, api_password, api_client_secret, api_base_url, api_client_id))  # Add API credentials to the set

    return api_password_values

def search_aws_credentials(strings_output):
    aws_credentials = set()  # Use a set to store unique AWS credentials

    # Patterns to match AWS credentials, considering potential multi-line definitions
    access_key_pattern = re.compile(r'["\']?accessKeyId["\']?\s*[:=]\s*["\']?([A-Z0-9]{16,20})["\']?', re.IGNORECASE)
    secret_key_pattern = re.compile(r'["\']?secretAccessKey["\']?\s*[:=]\s*["\']?([A-Za-z0-9/+=]{40})["\']?', re.IGNORECASE)
    session_token_pattern = re.compile(r'["\']?sessionToken["\']?\s*[:=]\s*["\']?([A-Za-z0-9/+=]+)["\']?', re.IGNORECASE)
    secret_key_var_pattern = re.compile(r'Qa_aws_secret_key\s*=\s*["\']?([A-Za-z0-9/+=]{40})["\']?|ll_aws_secret_key\s*=\s*["\']?([A-Za-z0-9/+=]{40})["\']?', re.IGNORECASE)

    # Temporary storage for keys
    temp_access_key = None
    temp_secret_key = None
    temp_session_token = "Unknown Session Token"

    for line in strings_output.splitlines():
        # Search for access key
        access_key_match = access_key_pattern.search(line)
        if access_key_match:
            temp_access_key = access_key_match.group(1)
        
        # Search for secret key directly
        secret_key_match = secret_key_pattern.search(line)
        if secret_key_match:
            temp_secret_key = secret_key_match.group(1)
        
        # Search for session token
        session_token_match = session_token_pattern.search(line)
        if session_token_match:
            temp_session_token = session_token_match.group(1)

        # Search for secret key defined as a variable
        secret_key_var_match = secret_key_var_pattern.search(line)
        if secret_key_var_match:
            temp_secret_key = secret_key_var_match.group(1) if secret_key_var_match.group(1) else secret_key_var_match.group(2)

        # Search for credentials in the specific format
        if 'accessKeyId' in line and 'll_aws_secret_key' in line:
            try:
                access_key = re.search(r'accessKeyId["\']?\s*[:=]\s*["\']?([A-Z0-9]{16,20})["\']?', line).group(1)
                secret_key = re.search(r'll_aws_secret_key\s*=\s*["\']?([A-Za-z0-9/+=]{40})["\']?', line).group(1)
                aws_credentials.add((access_key, secret_key, temp_session_token))
            except AttributeError:
                pass  # Skip if pattern not fully matched

        # If both access key and secret key are found, add to set and reset temp values
        if temp_access_key and temp_secret_key:
            aws_credentials.add((temp_access_key, temp_secret_key, temp_session_token))
            # Reset temp variables
            temp_access_key = None
            temp_secret_key = None
            temp_session_token = "Unknown Session Token"

    return aws_credentials
def search_bearer_token_with_context(strings_output):
    bearer_pattern = re.compile(r'blade-auth:\s*bearer\s*(\S+)|Authorization:\s*Bearer\s*(\S+)', re.IGNORECASE)
    lines = strings_output.splitlines()
    bearer_info = []

    for i, line in enumerate(lines):
        match = bearer_pattern.search(line)
        if match:
            # Check both groups for the token
            token = match.group(1) if match.group(1) else match.group(2)
            
            # Collect lines above until we find "GET" or "POST"
            above_lines = []
            for j in range(i - 1, -1, -1):
                above_lines.insert(0, lines[j])
                if 'get' in lines[j].lower() or 'post' in lines[j].lower() or 'GET' in lines[j] or 'POST' in lines[j]:
                    break
            
            # Collect lines below until we find "GET" or "POST"
            below_lines = []
            for j in range(i + 1, min(i + 3, len(lines))):  # Only collect up to 2 lines below
                below_lines.append(lines[j])

            context = {
                "token": token,
                "above": '\n'.join(above_lines),
                "below": '\n'.join(below_lines)
            }
            bearer_info.append(context)
    
    return bearer_info

def format_output(data_values, data_type):
    formatted_data_list = []
    seen = set()

    if data_type == 'password':
        for username, password in data_values:
            if (username, password) not in seen:
                seen.add((username, password))
                formatted_data_list.append(f'Username: "{username}", Password: "{password}"')
    elif data_type == 'client_id':
        for entry in data_values:
            client_id = entry.get("client_id")
            user_id = entry.get("user_id")
            client_secret = entry.get("client_secret")
            username = entry.get("username")
            password = entry.get("password")
            redirect_uris = entry.get("redirect_uris", [])

            unique_key = (client_id, user_id, client_secret, username, password, tuple(redirect_uris))

            if unique_key not in seen:
                seen.add(unique_key)

                formatted_entry = f'Client ID: "{client_id}"'
                if user_id:
                    formatted_entry += f'\n  User ID: "{user_id}"'
                if redirect_uris:
                    formatted_entry += ''.join(f'\n  Redirect URI: "{uri}"' for uri in redirect_uris)
                if client_secret and username and password:
                    formatted_entry += f'\n  Client Secret: "{client_secret}", Username: "{username}", Password: "{password}"'

                formatted_data_list.append(formatted_entry)
    elif data_type == 'api_password':
        for api_username, api_password, api_client_secret, api_base_url, api_client_id in data_values:
            if (api_username, api_password, api_client_secret, api_base_url, api_client_id) not in seen:
                seen.add((api_username, api_password, api_client_secret, api_base_url, api_client_id))
                formatted_data_list.append(f'API Username: "{api_username}", API Password: "{api_password}", API Client Secret: "{api_client_secret}", API Base URL: "{api_base_url}", API Client ID: "{api_client_id}"')
    elif data_type == 'bearer_token':
        for context in data_values:
            token = context["token"]
            above = context["above"]
            below = context["below"]

            unique_key = (token, above, below)

            if unique_key not in seen:
                seen.add(unique_key)
                formatted_data_list.append(f'{above}\n{token}\n{below}')
    elif data_type == 'aws_credentials':
        for access_key, secret_key, session_token in data_values:
            formatted_data_list.append(f'Access Key: "{access_key}", Secret Access Key: "{secret_key}", Session Token: "{session_token}"')

        return "\n\n".join(formatted_data_list)
    else:
        return "Invalid data type selected"

    formatted_data = '\n'.join(f'{index + 1}. {entry}' for index, entry in enumerate(formatted_data_list))
    return formatted_data

@app.route('/analyze', methods=['POST'])
def analyze_heap_dump():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    data_type = request.form.get('dataType')
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            strings_output = extract_strings_from_heapdump(filepath)
            if data_type == 'password':
                data_values = search_password_values(strings_output)
            elif data_type == 'client_id':
                data_values = search_client_ids(strings_output)
            elif data_type == 'api_password':
                data_values = search_api_password(strings_output)
            elif data_type == 'bearer_token':
                data_values = search_bearer_token_with_context(strings_output)
            elif data_type == 'aws_credentials':
                data_values = search_aws_credentials(strings_output)
            else:
                return jsonify({"error": "Invalid data type selected"}), 400

            if data_values:
                formatted_data = format_output(data_values, data_type)
                return jsonify({"message": formatted_data}), 200
            else:
                return jsonify({"message": f"No {data_type} data found"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=8080)

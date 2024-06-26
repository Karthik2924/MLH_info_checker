import requests
# API endpoint configuration
api_url = "https://transcribe.whisperapi.com"
headers = {'Authorization': 'Bearer JLSGXQ7476LBC3ILQTTPP44D7CE5EAU9'}

# Payload setup for API request
payload = {
    'file': {'file': open(r'YOUR_FILE_PATH', 'rb')}, 
    'data': {
        "fileType": "audio",  # Default is 'wav'.
        "diarization": "false",  # 'True' may slow down processing.
        "numSpeakers": "2",  # Optional: Number of speakers for diarization. If blank, model will auto-detect.
        #"url": "URL_OF_STORED_AUDIO_FILE",  # Use either URL or file, not both.
        "initialPrompt": "",  # Optional: Teach model a phrase. May negatively impact results.
        "language": "en",  # Optional: Language of speech. If blank, model will auto-detect.
        "task": "transcribe",  # Use 'translate' to translate speech from language to English. Transcribe is default.
        "callbackURL": "",  # Optional: Callback URL for results to be sent.
    }
}

# Ensure the 'callbackURL' starts with 'https://' and does not include 'www.'
# The server calls the callback URL once the response is ready.

# Make the API request and print the response
response = requests.post(api_url, headers=headers, files=payload['file'], data=payload['data'])
# Check if the request was successful (status code 200)
if response.status_code == 200:
    try:
        # Parse the JSON response
        json_response = response.json()
        # Extract the text content from the response if present
        text_content = json_response.get('text')
        if text_content:
            print("Text Content:", text_content)
        else:
            print("Text content not found in the response.")
    except ValueError:
        print("Invalid JSON response.")
else:
    print("Error occurred:", response.text)

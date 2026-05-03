import requests
import os

api_key = "AIzaSyB2wqTZ4QTqz3_VnwEKf2daIGOtXsze21w"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)
models = response.json().get('models', [])
for m in models:
    if 'generateContent' in m.get('supportedGenerationMethods', []):
        print(m.get('name'))

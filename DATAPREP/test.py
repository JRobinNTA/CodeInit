import requests
import json

url =  'http://localhost:11434/api/generate'

headers ={
    'Content-Type': 'application/json'
}

data ={
    'model': 'mistral',
    'prompt': 'hi there running test with ollama apis',
    'stream':False,
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    response_got = response.text
    data = json.loads(response_got)
    output = data['output']
    print(output)

else:
    print(f'error: {response.status_code}')
import requests
response = requests.get('https://huggingface.co', verify=False)
print(response.status_code)

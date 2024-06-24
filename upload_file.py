import requests

url = 'http://127.0.0.1:5000/upload'
files = {'file': open(r'C:\Users\Dor Shukrun\AllCoding\Exelanteam\Python\python_exc_5\final-exercise-DSH93\DEMO.pptx', 'rb')}
response = requests.post(url, files=files)

print(response.status_code)
print(response.text)

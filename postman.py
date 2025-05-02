import requests

url = "http://127.0.0.1:5000/predict"  # deployed server URL
file_path = "/home/surya/resumeScoring/uploads/HighScoringResume.pdf"  # path to your local PDF

with open(file_path, "rb") as f:
    files = {'file': (file_path, f, 'application/pdf')}
    response = requests.post(url, files=files)

print(response.json())

import requests



print(requests.get("http://127.0.0.1:8000/database").json())

#url = "https://www.google.com"
#url = url.replace("/","'",255)
#request = "http://127.0.0.1:8000/database/Add-url/" + url
#print(url)
#print(request)
#print(requests.post(request).json())
#request = "http://127.0.0.1:8000/check-status/" + url
#request = "http://127.0.0.1:8000/database/None-status/"

request = "http://127.0.0.1:8000/database/All-test/"
print(requests.get(request).json())

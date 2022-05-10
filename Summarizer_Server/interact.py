from urllib import response
import requests

def updateStatus(**kwargs):
    response = requests.post("http://127.0.0.1:8000/updatefilestatus/", json=kwargs)
    return

def getOldestRequest():
    response = requests.get("http://127.0.0.1:8000/getoldestrequest/")
    data = response.json()
    return data
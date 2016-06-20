import json
import requests
data = {
    "team_a": "1",
    "team_b": "2"
}
r = requests.put("https://sweltering-torch-9311.firebaseio.com/results.json", data=json.dumps(data))
print r.status_code
print r.content

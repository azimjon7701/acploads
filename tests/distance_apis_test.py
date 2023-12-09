import http.client

conn = http.client.HTTPSConnection("010pixel-distance-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "6212e81690msh4a423793bb301d4p1e3b7cjsn02365635278f",
    'X-RapidAPI-Host': "010pixel-distance-v1.p.rapidapi.com"
    }

conn.request("GET", "/?long1=-25.3&lat2=34.5&long2=-403.4&lat1=10&unit=K", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
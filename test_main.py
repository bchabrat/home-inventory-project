import requests

payload = {'name': 'Bathroom'}

post_r = requests.post('http://127.0.0.1:8000/room', auth=('bastien','chabrat'), params=payload)
print(post_r.status_code)
r = requests.get('http://127.0.0.1:8000/list_rooms', auth=('bastien','chabrat'))
print(r.status_code)
print(r.json())

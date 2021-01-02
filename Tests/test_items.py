import requests

payload = {'name':'pencil',
           'new_name':'pencil changed',
           'id':1,
           'room_id':1}
payload2 = {'name':'calculator',
           'id':3,
            'container_id':3,
           'room_id':1}
post_r = requests.post('http://127.0.0.1:8000/item', auth=('bastien','chabrat'), params=payload)
post_r = requests.post('http://127.0.0.1:8000/item', auth=('bastien','chabrat'), params=payload2)

print("status code for POST:",post_r.status_code)
r = requests.get('http://127.0.0.1:8000/list_items', auth=('bastien','chabrat'))
print("status code for GET:",r.status_code)
print("JSON for GET:",r.json())

r = requests.put('http://127.0.0.1:8000/item', auth=('bastien','chabrat'), params=payload)
print("status code for PUT:",r.status_code)

r = requests.get('http://127.0.0.1:8000/list_items', auth=('bastien','chabrat'))
print("status code for GET:",r.status_code)
print("JSON for GET:",r.json())

r = requests.delete('http://127.0.0.1:8000/item', auth=('bastien','chabrat'), params=payload2)
print("status code for delete:",r.status_code)

r = requests.get('http://127.0.0.1:8000/list_items', auth=('bastien','chabrat'))
print("status code for GET:",r.status_code)
print("JSON for GET:",r.json())

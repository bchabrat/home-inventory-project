import requests

payload = {'name': 'Bathroom'}

post_r = requests.post('http://127.0.0.1:8000/room', auth=('bastien','chabrat'), params=payload)
print("status code for POST:",post_r.status_code)
r = requests.get('http://127.0.0.1:8000/list_rooms', auth=('bastien','chabrat'))
print("status code for GET:",r.status_code)
print("JSON for GET:",r.json())
#
# payload = {'id':3,'name': 'Bathroom', 'new_name':"changedBathroom"}
# r = requests.put('http://127.0.0.1:8000/room', auth=('bastien','chabrat'), params=payload)
# print("status code for PUT:",r.status_code)
#
# r = requests.get('http://127.0.0.1:8000/list_rooms', auth=('bastien','chabrat'))
# print("status code for GET:",r.status_code)
# print("JSON for GET:",r.json())
#
# payload = {'id':3,'name': 'changed', 'new_name':"changedBathroom"}
# r = requests.delete('http://127.0.0.1:8000/room', auth=('bastien','chabrat'), params=payload)
# print("status code for delete:",r.status_code)
#
# r = requests.get('http://127.0.0.1:8000/list_rooms', auth=('bastien','chabrat'))
# print("status code for GET:",r.status_code)
# print("JSON for GET:",r.json())

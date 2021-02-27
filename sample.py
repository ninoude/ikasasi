import os
import subprocess
import requests
import time
import json
from IPython import embed
from elasticsearch import Elasticsearch

url = 'https://app.splatoon2.nintendo.net/api/results'
cookie = {'iksm_session': os.environ['IKSM_SESSION']}
response = requests.get(url=url,  cookies=cookie)
json_data = response.json()
battle_number = json_data['results'][0]['battle_number']

es = Elasticsearch(host="localhost", port=9200)
if es.indices.exists(index="splatoon2"):
	pass
else:
	es.indices.create(index='splatoon2')

for i in range(50):
	num = int(battle_number) - i
	res_url = url + '/' + str(num)
	r = requests.get(url=res_url,  cookies=cookie)
	json_data = r.json()
	es.index(index='splatoon2', body=json_data)
	time.sleep(1)
es.close()

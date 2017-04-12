import requests
import json

def get_categories():
	url = 'http://youtubesweg.me/api/category'
	listHolder = list()
	r = requests.get(url)
	for x in r.json():
		for y in x:
			if y == 'categories':
				for z in x[y]:
					tempdict = {}
					tempdict['title'] = z['title']
					tempdict['channels'] = z['channels'] 
					print(tempdict['title'])
					print(tempdict['channels'])

get_categories()
##print(r.json())
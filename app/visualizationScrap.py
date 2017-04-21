import requests
import json
import sys

def get_data():
    data = {"name": "Categories", "children":[]}
    categories_list = get_categories()
    for x in categories_list:
        tempdict = {}
        templist = []
        tempdict["name"] = x["title"]
        url = 'http://youtubesweg.me/api/channel?id='
        tempdict["children"] = []
        for y in x["channels"]:
            url = url + str(y) + ','
        r = requests.get(url)
        rjson = r.json()[0]["channels"]
        for entry in rjson:
            tempdict2 = {}
            tempdict2["name"] = entry["title"]
            tempdict2["children"] = []
            list_of_videos = entry["videos"]
            view_count = entry["view_count"]
            url2 = 'http://youtubesweg.me/api/video?id='
            for z in list_of_videos:
                url2 = url2 +str(z)+','
            r2 = requests.get(url2)
            r2json = r2.json()[0]["videos"]
            for entry2 in r2json:
                tempdict3 = {}
                tempdict3["name"] = entry2["title"]
                tempdict3["size"] = view_count // len(list_of_videos)
                tempdict2["children"] += [tempdict3]
            tempdict["children"] += [tempdict2]
        data["children"] += [tempdict]
    with open('templates/flare.json', 'w') as data_file:
        json.dump(data, data_file)




def get_categories():
    url = 'http://youtubesweg.me/api/category'
    listHolder = list()
    r = requests.get(url)
    for x in r.json():
        for y in x:
            if y == 'categories':
                for z in x[y]:
                    tempdict = {}
                    tempdict["title"] = z["title"]
                    tempdict["channels"] = z["channels"]
                    listHolder += [tempdict]
    return listHolder


def get_channels():
    url = 'http://youtubesweg.me/api/channel'
    listHolder = list()
    r = requests.get(url)
    for x in r.json():
        for y in x:
            if y == 'channels':
                for z in x[y]:
                    tempdict = {}
                    tempdict['id'] = z['id']
                    tempdict['title'] = z['title']
                    tempdict['videos'] = z['videos']
                    tempdict['view_count'] = z['view_count']
                    listHolder += [tempdict]
    return listHolder


def get_videos():
    url = 'http://youtubesweg.me/api/video'
    listHolder = list()
    r = requests.get(url)
    for x in r.json():
        for y in x:
            if y == 'videos':
                for z in x[y]:
                    tempdict = {}
                    tempdict['id'] = z['id']
                    tempdict['title'] = z['title']
                    tempdict['video_url'] = z['video_url']
                    listHolder += [tempdict]
    return listHolder

# output = [
#     {'categories': get_categories(), 'channels': get_channels(), 'videos': get_videos()}]
get_data()

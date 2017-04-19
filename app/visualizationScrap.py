import requests
import json
import sys


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

output = [
    {'categories': get_categories(), 'channels': get_channels(), 'videos': get_videos()}]
print(output)

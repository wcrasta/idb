import requests
import json
import sys
def scrape(name):
    headers = {
       'X-Mashape-Key': 'SabC5JsP3Rmsh34Z4U1wuqMgiBDNp18DhDsjsnxxeyvtNQKxOM'
    }
    output = []
    index = 0
    errorcount = 0
    print(sys.argv)
    while True:
        url = 'https://igdbcom-internet-game-database-v1.p.mashape.com/'+name+'/'
        for i in range(index+1, index+1001):
            url += str(i) + ','
        url = url[0:len(url)-1]
        url += '/?fields=*'
        r = requests.get(url, headers=headers)
        parsed_json = r.json()
        print(index)
        index += 1000
        for entry in parsed_json:
            try:
                x = entry['error']
                errorcount+=1
                if errorcount>200:
                    break
            except (KeyError,TypeError):
                print(entry)
                output.append(entry)
                errorcount = 0
        if errorcount > 200:
            break
    #for entry in output:
        #print(entry["name"])
    print(len(output))
    with open(name+'.json', 'w', encoding='utf-8') as f:
        json.dump(output, f,ensure_ascii=False)

scrape(sys.argv[1])

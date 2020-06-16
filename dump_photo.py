import json
import requests
import os
import sys

jsonReq = """
{
    "reportId":"weightingReport",
    "from":"2018-11-14T20:00:00.000Z",
    "to":"2018-11-16T20:00:00.000Z",
    "entityId":[],
    "strEntityId":[],
    "filters":{
        "unitId":null
        }
}

"""
site = sys.argv[1]
api = sys.argv[2]
from_date = "%sT00:00:00.000Z" % sys.argv[3]
to_date = "%sT00:00:00.000Z" % sys.argv[4]

jreq = json.loads(jsonReq)
jreq['from'] = from_date
jreq['to'] = to_date


geturl = "https://%s/data/reportData?apiKey=%s&reportId=weightingReport" % (site, api)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(geturl, data=json.dumps(jreq), headers=headers)


for i in r.json()['data']:
    image2list = str(i['images2']).split('<br>')
    for image in image2list:
        if image:
            imagelist = image.split('/')
        else:
            continue
        if not os.path.isdir(imagelist[3]):
            os.mkdir(imagelist[3])
            print("Dir created: " + imagelist[3])
        os.system("wget -q http://%s/%s -P %s/" % (site, image, imagelist[3]))
        print("Downloaded: " + imagelist[4])

os.system('for i in */; do zip -r "${i%/}.zip" "$i"; done && for i in */; do rm -rf "${i%/}" "$i"; done')



import urllib.request
import urllib.parse

# post提交的参数：
data = {
    "query": "blockchain",
    "queryExpression": "",
    "filters": [],
    "orderBy": 0,
    "skip": 0,
    "sortAscending": True,
    "take": 10
}

data = urllib.parse.urlencode(data).encode()

url = r'https://academic.microsoft.com/api/search'

headers = {
           # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en',
           'accept': 'application/json',
           'content-type': 'application/json; charset=utf-8',
           'x-requested-with': 'Fetch',
           # ':authority': 'academic.microsoft.com',
           # ':method': 'POST',
           # ':path': '/api/search',
           # ':scheme': 'https',
           'cookie': 'MC1=GUID=339a2beaba4a434ba977825f62ec8d92&HASH=339a&LV=201904&V=4&LU=1556179668855; MUID=1C7924856B4765180E9229CC6F4763D2; ai_user=ozO7e|2019-05-11T12:12:31.286Z; MSCC=1557576805; ai_session=GfP7U|1557584928304.365|1557584928304.365',
           'origin': 'https://academic.microsoft.com',
           'referer': 'https://academic.microsoft.com/search?q=blockchain&f=&orderBy=0&skip=20&take=10',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
           }

request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request, data=data)

print(response.getcode())
print(response.read().decode())

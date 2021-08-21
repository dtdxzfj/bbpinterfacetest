import requests
import json

bbp_header = {'User-Agent': "Chrome/89.0.4389.72", 'Content-Type': 'application/json', "charset": "UTF-8",
              "authorization": '36906015a22b43c5b05835cceaa22e47',
              'token': 'eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJjb20ueGRmLmJsaW5nIiwiYXVkIjoiY2xpZW50IiwidXNlcmNvZGUiOiJjcm10ZXN0YWRtaW4iLCJleHAiOjE2MjI0NDgzODQsImlhdCI6MTYyMTIzODc4NH0.SvV2FbwyhWxMTNFfcQnPO6X321qmvl1eYN54s11OIBH6ige1j3bchXUxVMcDIKnRBbaOMRl4r-yUv3vcBqfKFA'}

url = 'https://oapi-alpha.t.blingabc.com/foreign/admin-api/teacher/v1/teachers'
data = json.dumps(
    {"groupIds": [], "ifNotGrouped": True, "crmAdminUserId": 20, "page": 1, "size": 500, "teacherStatus": 1})
req = json.loads(requests.request('POST', url=url, data=data, headers=bbp_header).text)['data']['list']
techeridlist = []
urll = 'https://oapi-alpha.t.blingabc.com/share-schedule/user-api/scheduleclass/v1/foreignteacher/timecount'
for item in req:
    listdata = json.dumps({
        "foreignTeacherId": item['id'],
        "year": 2021,
        "term": 10
    })
    # 外教可用时间开放量（少的优先），目前查询的数据只有春秋的，其他的没有配置
    reqqq = json.loads(requests.request('POST', url=urll, data=listdata, headers=bbp_header).text)
    print(item['id'], reqqq)





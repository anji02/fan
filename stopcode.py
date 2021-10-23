# -*- coding: UTF-8 -*-
# 开发时间：2021/10/22 4:31
# 本地获取token
import requests
import sys
import time
import json
'''
cron: 15 */8 * * * stopcode.py   15 * * * *
new Env('停止code');
'''

headers={
    "Accept":        "application/json",
    'Content-Type': "application/json;charset=UTF-8",
    "Authorization": "Basic YWRtaW46YWRtaW4=",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
}
ql_ip = '127.0.0.1:5700'
def loadToken():
    # cur_path = os.path.abspath(os.path.dirname(__file__))
    # send("当前路径：",cur_path)
    try:
        with open("/ql/config/auth.json","r",encoding="utf-8") as f:
            data=json.load(f)
    except:
        # pass
        print("无法获取token, 请检测青龙配置")
    return data['token']

def searchcode():
    try:
        # 查询code.sh是否在运行
        t = round(time.time() * 1000)
        url = 'http://{0}/api/crons?searchValue=code.sh&t={1}'.format(ql_ip, t)
        response = requests.get(url=url, headers=headers)
        responseContent = json.loads(response.content.decode('utf-8'))
        if responseContent['code'] == 200:
            taskList = responseContent['data']
            return taskList
        else:
            # 没有获取到taskList，返回空
            return []
    except:
        print('未查询到code.sh,请检测青龙任务列表...')
        sys.exit(0)

def stp(eid):
    try:
        t = round(time.time() * 1000)
        url = 'http://{0}/api/crons/stop?t={1}'.format(ql_ip, t)
        data = []
        data.append(eid)
        data = json.dumps(data)
        response = requests.put(url=url, headers=headers, data=data)
        print(response.text)
        responseContent = json.loads(response.content.decode('utf-8'))
        if responseContent['code'] == 200:
            print('成功停止')
    except:
        print('无法停止，请检测code.sh状态')
        sys.exit(0)

if __name__ == '__main__':
    token=loadToken()
    headers["Authorization"] = "Bearer %s" % token
    taskList=searchcode()
    eid = taskList[0]["_id"]
    print("code.sh任务[_id]:"+eid)
    status = taskList[0]["status"]
    if status==0:
        stp(eid)
    else:
        print('code.sh状态[status:{0}]，暂未运行'.format(status))
        sys.exit(0)
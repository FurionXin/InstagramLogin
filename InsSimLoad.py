# coding:utf-8
# If the following error occurs during running：
# requests.exceptions.SSLError: [Errno 1] _ssl.c:510: error:14090086:SSL
# please set-up requests like this:response = requests.get(url_login,allow_redirects=False,verify=False)
import requests
import re
import json
from urllib import unquote

url_login = 'https://www.instagram.com/oauth/authorize/?client_id=c0a94fa83f674942ba7b41d184b8a455&redirect_uri=https://polar-shelf-32169.herokuapp.com/api/v1/instagram/oauth_redirect&response_type=code&scope=basic+public_content+follower_list+relationships+comments+likes'
def insload(username,password):
    response = requests.get(url_login,allow_redirects=False)
    headers_json = json.loads(json.dumps(eval(str(response.headers))))
    location1_str = headers_json['Location']
    set_cookie = str(headers_json['Set-Cookie'])
    csrftoken1_str = str(re.compile(r"csrftoken=(.+?);").findall(set_cookie))
    mid_str = str(re.compile(r"mid=(.+?);").findall(set_cookie))
    insload_second(location1_str,csrftoken1_str,mid_str,username,password)

def insload_second(location1_str,csrftoken1_str,mid_str,username,password):
    Headers = {
        "referer": location1_str,
        "Origin": "https://www.instagram.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate"}
    cookies_first = {"csrftoken": csrftoken1_str[2:len(csrftoken1_str)-2:],
                     "mid": mid_str[2:len(mid_str)-2:]}
    body_first = {"csrfmiddlewaretoken": csrftoken1_str[2:len(csrftoken1_str)-2:],
              "username": username,
              "password": password}
    response = requests.post(location1_str, cookies=cookies_first, headers=Headers, data=body_first, allow_redirects=False)
    headers_json = json.loads(json.dumps(eval(str(response.headers))))
    set_cookie = str(headers_json['Set-Cookie'])
    csrftoken2_str = str(re.compile(r"csrftoken=(.+?);").findall(set_cookie))
    sessionid_str = str(re.compile(r"sessionid=(.+?);").findall(set_cookie))
    if sessionid_str[2:3:] != ';':
        location2_str = headers_json['Location']
        insload_third(location2_str, csrftoken2_str, mid_str, sessionid_str)
    else:
        print "The username or password you entered is incorrect. Please re-enter it."
        inputAccount()

def insload_third(location2_str,csrftoken2_str,mid_str,sessionid_str):
    Headers = {
        "referer": location2_str,
        "Origin": "https://www.instagram.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate"}
    cookies_first = {"csrftoken": csrftoken2_str[2:len(csrftoken2_str)-2:],
                     "mid": mid_str[2:len(mid_str)-2:],
                     "sessionid": sessionid_str[2:len(sessionid_str)-2:]}
    response = requests.get(location2_str,cookies=cookies_first,headers=Headers,allow_redirects=False)
    headers_json = json.loads(json.dumps(eval(str(response.headers))))
    location3_str = headers_json['Location']
    insload_finish(location3_str)

def insload_finish(location3_str):
    response = requests.get(location3_str, allow_redirects=False)
    access_token = str(re.compile(r"access_token=(.*?)$").findall(str(response.content)))
    full_name = str(re.compile(r"full_name=(.+?)&").findall(str(response.content)))
    username = str(re.compile(r"username=(.+?)&").findall(str(response.content)))
    print "your access_token is: "+access_token[2:len(access_token)-2:]
    print "your full_name is: "+unquote(full_name[2:len(full_name)-2:])
    print "your username is: "+username[2:len(username)-2:]

def inputAccount():
    username = raw_input("please input your username:")
    password = raw_input("please input your password:")
    print "please wait for a moment~~"
    insload(username, password)

if __name__ == '__main__':
    inputAccount()

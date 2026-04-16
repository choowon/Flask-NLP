import requests
import csv
import os
import numpy as np
def init():
    if not os.path.exists('navData.csv'):
        with open('navData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'typeName',
                'gid',
                'containerid'
            ])

def wirterRow(row):
        with open('navData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",

        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",

        "Referer": "https://weibo.com/mygroups?gid=110005270095497",

        "Client-Version": "3.0.0",
        "Server-Version": "v2026.04.13.3",

        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-Token": "9sg6zwsLOvFwgOGpMLMVwh9c",

        "Cookie": "SINAGLOBAL=2626454965714.534.1761749213102; SCF=Ancboj1AhtvTO6pHcFGG-vtKeAZUImwcdbD698GdkZp7QxdVEX-Y2JZj4SS5rxNvUSr-wZr-_97v-Qw9YSrcn98.; XSRF-TOKEN=9sg6zwsLOvFwgOGpMLMVwh9c; PC_TOKEN=c304ce5a67; _s_tentry=-; Apache=5843468602523.462.1776093323168; ULV=1776093323169:3:1:1:5843468602523.462.1776093323168:1764580004438; SUB=_2A25E2XjyDeRhGeNM7FIR-SvIwjuIHXVnl_Q6rDV8PUNbmtANLWfmkW9NThXdIASjYoE7F3dIMhPxQxAvEIEMTYqT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFJAAl1usp_k7Xl4IqKRs755JpX5KzhUgL.Fo-ES0571K-X1KM2dJLoI0qLxKqL1h.LBKMLxKnL1K2L1KMLxKML1-2L1hBLxKnLB--LBo5LxKBLB.2L12zLxKqL1-eLB-et; ALF=02_1778685346; WBPSESS=CgCEolsEIXqpGGXF65Yc68Zb3s7RqJov3tyIPm128KWOer5KZHCT9b_nOfAXQcT90CGBhp3ifBRHPXEPwVPR5ReDW-mm5BjMPvw17aacHrZAZMqojzrUf0DVsumteBSAlhYUCwrUrDlJNaJuIOVtUg=="
    }
    params = {
        'is_new_segment':1,
        'fetch_hot':1
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        wirterRow([
            navName,
            gid,
            containerid,
        ])

if __name__ == '__main__':
    url = 'https://weibo.com/ajax/feed/allGroups'
    init()
    response = get_html(url)
    parse_json(response)
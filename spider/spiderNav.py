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
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'Cookie':'SCF=AnQ2qSn180Dge9MwgUCdoA4mBqCM89aMBSgYzFlXYZOgSo90ToHWO-YmGpOr6xilWmftjUdocQMYKgakhiadRms.; SINAGLOBAL=7727468373074.708.1732304263493; ULV=1743155382749:11:9:3:9358840925073.043.1743155382745:1743129658946; XSRF-TOKEN=Tp4fLatnTgzVv11OGvVIvghK; PC_TOKEN=f454524860; SUB=_2A25FVWw8DeRhGeNM41ET9ijEyTSIHXVmK-H0rDV8PUNbmtAYLUmjkW9NSeBYP2FUov0S_inRZzpbEH7oCiGjCzpR; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Rg7xsxXaus_JFlT2Fe0Mn5JpX5KzhUgL.Fo-E1heESoqReon2dJLoIE-LxK.LBKeLB-qLxK-LB-qLBoqLxK-L122L12xk-s8EIXiaxNH_; ALF=02_1752738156; WBPSESS=HpkzK1RdxrD5A-fhn3HDjt1t-KMAeYXOfAVxAmOfnoXSbx8ng-zlVoIvUWJNRFdKb5z0SepO-sTMZVtt5GuaBpoQy6wtSaY0XBYHOIO6QnYrFvnOOKEGBv46cTNrQKXe7SLEz9EVdBDto1hqQS6U0Q=='
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
import requests
import csv
import os
from datetime import datetime
def init():
    if not os.path.exists('commentsData.csv'):
        with open('commentsData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'articleId',
                'created_at',
                'like_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])

def wirterRow(row):
        with open('commentsData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

def get_html(url,id):
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
        'is_show_bulletin':2,
        'id':id
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response,articleId):
    commentList = response['data']
    for comment in commentList:
        created_at = datetime.strptime(comment['created_at'],"%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        like_counts = comment['like_counts']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location'].split(' ')[0]
        authorAvatar = comment['user']['avatar_large']
        try:
            region = comment['source'].replace('来自','')
        except:
            region = '无'
        content = comment['text_raw']
        wirterRow([
            articleId,
            created_at,
            like_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar,
        ])

def start():
    init()
    url = 'https://weibo.com/ajax/statuses/buildComments'
    with open('./articleData.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for article in reader:
            articleId = article[0]
            response = get_html(url,articleId)
            parse_json(response,articleId)


if __name__ == '__main__':
    start()
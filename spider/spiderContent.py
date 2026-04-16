import time
import requests
import csv
import os
import re
from datetime import datetime
def init():
    if not os.path.exists('articleData.csv'):
        with open('articleData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'id',
                'likeNum',
                'commentsLen',
                'reposts_count',
                'region',
                'content',
                'contentLen',
                'created_at',
                'type',
                'detailUrl',# followBtnCode>uid + mblogid
                'authorAvatar',
                'authorName',
                'authorDetail',
                'isVip' # v_plus
            ])

def wirterRow(row):
        with open('articleData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

def get_json(url,params):
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
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None

def parse_json(response,type):
    for article in response:
        id = article['id']
        likeNum = article['attitudes_count']
        commentsLen = article['comments_count']
        reposts_count = article['reposts_count']
        try:
            region = article['region_name'].replace('发布于 ','')
        except:
            region = '无'
        content = article['text_raw']
        contentLen = article.get('textLength', 0)
        created_at = datetime.strptime(article['created_at'],"%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        type = type
        try:
            detailUrl = 'https://weibo.com/' + str(article['user']['id']) +'/'+ str(article['mblogid'])
        except:
            detailUrl = '无'
        authorAvatar = article['user']['avatar_large']
        authorName = article['user']['screen_name']
        authorDetail = 'https://weibo.com' + article['user']['profile_url']
        if  article['user']['v_plus']:
            isVip = article['user']['v_plus']
        else:
            isVip = 0
        wirterRow([
                id,
                likeNum,
                commentsLen,
                reposts_count,
                region,
                content,
                contentLen,
                created_at,
                type,
                detailUrl,
                authorAvatar,
                authorName,
                authorDetail,
                isVip
            ])

def start(typeNum=2,pageNum=2):
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    typeNumCount = 0
    with open('./navData.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for nav in reader:
            if typeNumCount > typeNum:return
            for page in range(0,pageNum):
                time.sleep(2)
                print('正在爬取类型：' + nav[0] + '中的第' + str(page + 1) + '页数据')
                params = {
                    'group_id':nav[1],
                    'containerid':nav[2],
                    'max_id':page,
                    'count':10,
                    'extparam':'discover|new_feed'
                }
                response = get_json(articleUrl,params)
                parse_json(response['statuses'],nav[0])
            typeNumCount += 1

if __name__ == '__main__':
    start()
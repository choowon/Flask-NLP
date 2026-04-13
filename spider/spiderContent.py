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
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'Cookie':'SCF=AnQ2qSn180Dge9MwgUCdoA4mBqCM89aMBSgYzFlXYZOgSo90ToHWO-YmGpOr6xilWmftjUdocQMYKgakhiadRms.; SINAGLOBAL=7727468373074.708.1732304263493; ULV=1743155382749:11:9:3:9358840925073.043.1743155382745:1743129658946; XSRF-TOKEN=Tp4fLatnTgzVv11OGvVIvghK; PC_TOKEN=f454524860; SUB=_2A25FVWw8DeRhGeNM41ET9ijEyTSIHXVmK-H0rDV8PUNbmtAYLUmjkW9NSeBYP2FUov0S_inRZzpbEH7oCiGjCzpR; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Rg7xsxXaus_JFlT2Fe0Mn5JpX5KzhUgL.Fo-E1heESoqReon2dJLoIE-LxK.LBKeLB-qLxK-LB-qLBoqLxK-L122L12xk-s8EIXiaxNH_; ALF=02_1752738156; WBPSESS=HpkzK1RdxrD5A-fhn3HDjt1t-KMAeYXOfAVxAmOfnoXSbx8ng-zlVoIvUWJNRFdKb5z0SepO-sTMZVtt5GuaBpoQy6wtSaY0XBYHOIO6QnYrFvnOOKEGBv46cTNrQKXe7SLEz9EVdBDto1hqQS6U0Q=='
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
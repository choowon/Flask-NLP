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
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'Cookie':'SCF=AnQ2qSn180Dge9MwgUCdoA4mBqCM89aMBSgYzFlXYZOgSo90ToHWO-YmGpOr6xilWmftjUdocQMYKgakhiadRms.; SINAGLOBAL=7727468373074.708.1732304263493; ULV=1743155382749:11:9:3:9358840925073.043.1743155382745:1743129658946; XSRF-TOKEN=Tp4fLatnTgzVv11OGvVIvghK; PC_TOKEN=f454524860; SUB=_2A25FVWw8DeRhGeNM41ET9ijEyTSIHXVmK-H0rDV8PUNbmtAYLUmjkW9NSeBYP2FUov0S_inRZzpbEH7oCiGjCzpR; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Rg7xsxXaus_JFlT2Fe0Mn5JpX5KzhUgL.Fo-E1heESoqReon2dJLoIE-LxK.LBKeLB-qLxK-LB-qLBoqLxK-L122L12xk-s8EIXiaxNH_; ALF=02_1752738156; WBPSESS=HpkzK1RdxrD5A-fhn3HDjt1t-KMAeYXOfAVxAmOfnoXSbx8ng-zlVoIvUWJNRFdKb5z0SepO-sTMZVtt5GuaBpoQy6wtSaY0XBYHOIO6QnYrFvnOOKEGBv46cTNrQKXe7SLEz9EVdBDto1hqQS6U0Q=='
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
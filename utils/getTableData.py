from model.bert_predictor import bert_predict
from utils.getPublicData import *
from datetime import datetime
from snownlp import SnowNLP

def getTableDataPageData():
    return getAllCiPingTotal()

def getTableData(hotWord):
    commentList = getAllCommentsData()
    tableData =[]
    for comment in commentList:
        if comment[4].find(hotWord) != -1:
            tableData.append(comment)
    return tableData

def getTableDataEchartsData(hotWord):
    tableList = getTableData(hotWord)
    xData = [x[1] for x in tableList]
    xData = list(set(xData))
    xData = list(sorted(xData,key=lambda x:datetime.strptime(x,'%Y-%m-%d').timestamp(),reverse=True))
    yData = [0 for x in range(len(xData))]
    for comment in tableList:
        for index,x in enumerate(xData):
            if comment[1] == x:
                yData[index] += 1
    return xData,yData


# utils/getTableData.py

from model.bert_predictor import bert_predict
from utils.getPublicData import getAllData
from snownlp import SnowNLP
import os
import json

def getTableDataArticle(flag):
    tableListOld = getAllData()

    if not flag:
        return tableListOld

    # 缓存文件路径
    cache_path = 'cache/tableDataArticle.json'

    # 如果缓存存在，直接加载
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 否则重新生成
    contents = [item[5] for item in tableListOld]
    emotions_bert = bert_predict(contents)

    tableList = []
    for item, emotion_bert in zip(tableListOld, emotions_bert):
        item = list(item)
        content = item[5]

        # SnowNLP 预测
        sn_score = SnowNLP(content).sentiments
        emotion_snownlp = '正面' if sn_score > 0.5 else '负面'

        item.append(emotion_bert)
        item.append(emotion_snownlp)
        tableList.append(item)

    # 保存缓存
    os.makedirs('cache', exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(tableList, f, ensure_ascii=False, indent=2)

    return tableList


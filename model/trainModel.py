import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from snownlp import SnowNLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc
)
from sklearn.model_selection import train_test_split

# 创建保存图表的目录
os.makedirs("images", exist_ok=True)

def getSentiment_data():
    sentiment_data = []
    with open('./target.csv', 'r', encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        for data in reader:
            sentiment_data.append(data)
    return sentiment_data


def model_train(draw=True):
    sentiment_data = getSentiment_data()
    df = pd.DataFrame(sentiment_data, columns=['text', 'sentiment'])

    # 显示标签分布图
    if draw:
        plt.figure(figsize=(6, 4))
        sns.countplot(x='sentiment', data=df)
        plt.title("情感标签分布")
        plt.xlabel("情感标签")
        plt.ylabel("样本数量")
        plt.tight_layout()
        plt.savefig("images/label_distribution.png")
        plt.close()

    # 二分类处理：假设标签为字符串，需要转为整数
    label_mapping = {label: i for i, label in enumerate(df['sentiment'].unique())}
    df['label'] = df['sentiment'].map(label_mapping)

    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])

    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(train_data['text'])
    y_train = train_data['label']
    X_test = vectorizer.transform(test_data['text'])
    y_test = test_data['label']

    # LogisticRegression 支持概率预测和多轮迭代
    classifier = LogisticRegression(max_iter=100)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    y_proba = classifier.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    print(f"准确率：{accuracy:.4f}")

    # 混淆矩阵
    if draw:
        cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_mapping.keys())
        disp.plot(cmap='Blues')
        plt.title("混淆矩阵")
        plt.tight_layout()
        plt.savefig("images/confusion_matrix.png")
        plt.close()

    # ROC 曲线
    if draw:
        fpr, tpr, thresholds = roc_curve(y_test, y_proba)
        roc_auc = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('假阳性率')
        plt.ylabel('真阳性率')
        plt.title('ROC 曲线')
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig("images/roc_curve.png")
        plt.close()

    return vectorizer, classifier, label_mapping


def sentiment_analysis(text):
    vectorizer, classifier, label_mapping = model_train(draw=False)
    text_vector = vectorizer.transform([text])
    sentiment_idx = classifier.predict(text_vector)[0]
    # 反向映射标签
    inv_label_mapping = {v: k for k, v in label_mapping.items()}
    return inv_label_mapping[sentiment_idx]


if __name__ == "__main__":
    input_text = "什么破烂玩意？"
    result = sentiment_analysis(input_text)
    print("SnowNLP 情绪值（0=负面，1=正面）:", SnowNLP(input_text).sentiments)
    print("预测情感：", result)

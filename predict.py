import torch
from transformers import BertTokenizer
from model import SentimentClassifier
from snownlp import SnowNLP  # 引入 snownlp

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = BertTokenizer.from_pretrained('./model/bert-base-chinese')

def load_model(model_class, path='./model/sentiment_model.pth', device=device):
    model = model_class()
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device)
    model.eval()
    return model

def predict_bert(text):
    """ 使用 BERT 进行情感预测 """
    model = load_model(SentimentClassifier, device=device)

    inputs = tokenizer(text,
                       truncation=True,
                       padding='max_length',
                       max_length=500,
                       return_tensors='pt')
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    token_type_ids = inputs['token_type_ids'].to(device)

    with torch.no_grad():
        output = model(input_ids, attention_mask, token_type_ids)
        pred = output.argmax(dim=1).item()
        prob = output[0][pred].item()

    sentiment = "正面" if pred == 1 else "负面"
    return sentiment, prob


def predict_snownlp(text):
    """ 使用 snownlp 进行情感预测 """
    snownlp_result = SnowNLP(text).sentiments
    sentiment = "正面" if snownlp_result >= 0.5 else "负面"
    return sentiment, snownlp_result


def compare_predictions(text):
    """ 比较 BERT 和 snownlp 的预测结果 """
    print(f"\n文本：{text}")

    # BERT 预测
    sentiment_bert, prob_bert = predict_bert(text)
    print(f"BERT 预测：{sentiment_bert}，置信度：{prob_bert:.4f}")

    # snownlp 预测
    sentiment_snownlp, prob_snownlp = predict_snownlp(text)
    print(f"snownlp 预测：{sentiment_snownlp}，置信度：{prob_snownlp:.4f}")


if __name__ == '__main__':
    compare_predictions("这个产品真的太棒了，我非常满意！")
    compare_predictions("服务态度差，物流慢，一星都不想给！")


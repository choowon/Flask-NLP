# model/bert_predictor.py

import os
import json
import torch
from transformers import BertTokenizer
from model import SentimentClassifier

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = None
tokenizer = None

def load_model_once():
    global model, tokenizer
    if model is None or tokenizer is None:
        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        model_instance = SentimentClassifier()
        model_path = os.path.join("model", "sentiment_model_best.pth")
        # model_instance.load_state_dict(torch.load(model_path, map_location=device))
        model_instance.load_state_dict(
            torch.load(model_path, map_location=device),
            strict=False
        )
        model_instance.to(device)
        model_instance.eval()
        model = model_instance

def bert_predict(texts, batch_size=32):
    """
    批量预测文本情感（懒加载模型，自动分批）
    :param texts: List[str]
    :return: List[str] ['正面' or '负面']
    """
    load_model_once()
    results = []

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        inputs = tokenizer(batch_texts,
                           truncation=True,
                           padding='max_length',
                           max_length=256,  # 优化处理速度
                           return_tensors='pt')

        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)
        token_type_ids = inputs['token_type_ids'].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask, token_type_ids)
            preds = outputs.argmax(dim=1).tolist()

        results.extend(['正面' if p == 1 else '负面' for p in preds])

    return results

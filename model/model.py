import torch
from transformers import BertModel

class SentimentClassifier(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = BertModel.from_pretrained('model/bert-base-chinese')
        for param in self.bert.parameters():
            param.requires_grad_(False)
        self.fc = torch.nn.Linear(768, 2)

    def forward(self, input_ids, attention_mask, token_type_ids):
        with torch.no_grad():
            out = self.bert(input_ids=input_ids,
                            attention_mask=attention_mask,
                            token_type_ids=token_type_ids)
        cls_token = out.last_hidden_state[:, 0]
        logits = self.fc(cls_token)
        return logits.softmax(dim=1)

import joblib
from transformers import AutoTokenizer, AutoModel
import torch

# load lại model + encoder
saved = joblib.load("intent_classifier.pkl")
clf = saved["model"]
label_encoder = saved["label_encoder"]

# load trực tiếp từ thư mục local
tokenizer = AutoTokenizer.from_pretrained("./phobert-base-offline")
model = AutoModel.from_pretrained("./phobert-base-offline")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
    return cls_embedding.cpu().squeeze().numpy()

# thử dự đoán
while True:
    user_input = input("Bạn muốn điều khiển gì? ")  
    
    if user_input.lower() in ['exit', 'quit']:
        break

    text = user_input
    vector = get_embedding(text)
    label_num = clf.predict([vector])[0]
    intent = label_encoder.inverse_transform([label_num])[0]

    print("Intent dự đoán:", intent)

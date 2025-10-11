import joblib
from transformers import AutoTokenizer, AutoModel
import torch
from input_sound_processor import STT

# # B1: Tải tokenizer & model từ Hugging Face Hub
# tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
# model = AutoModel.from_pretrained("vinai/phobert-base")

# # B2: Lưu về thư mục local
# tokenizer.save_pretrained("./phobert-base-offline")
# model.save_pretrained("./phobert-base-offline")

# load lại model + encoder
saved = joblib.load("intent_classifier.pkl")
clf = saved["model"]
label_encoder = saved["label_encoder"]

# load trực tiếp từ thư mục local
tokenizer = AutoTokenizer.from_pretrained("./phobert-base-offline")
model = AutoModel.from_pretrained("./phobert-base-offline")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

def get_embedding(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
    return cls_embedding.cpu().squeeze().numpy()

# thử dự đoán
if __name__ == '__main__':
    stt = STT()
    while True:
        print("===== Options =====")
        print("1: Tạo lệnh bằng cách nhập chữ")
        print("2: Taọ lệnh bằng giọng nói")
        print("0: Thoát")
        
        try:           
            option = int(input("Vui lòng chọn số"))
        except ValueError:
            print('Vui lòng nhập số hợp lệ')
            continue
        if option == 0:
            break
        elif option == 1:
            user_input = input("Bạn muốn điều khiển gì? ").strip()  
        elif option == 2:
            user_input = stt.stt(filename=None, save=False) # nói trực tiếp không lưu 
        else:
            print("lựa chọn không hợp lệ")
            continue

        if not user_input:
            print("không nhận được lệnh")
            continue
        
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # dự đoán intent
        vector = get_embedding(user_input)
        label_num = clf.predict([vector])[0]
        intent = label_encoder.inverse_transform([label_num])[0]

        print("lệnh của bạn là ", user_input)
        print("Intent dự đoán:", intent)
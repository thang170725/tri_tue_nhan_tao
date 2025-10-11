# hướng dẫn run project

# Yêu cầu: 
#           máy tính đã cài đặt Python 3.8+ nên cài python 3.10 cho đồng bộ. 
#           Có chạy được python trên vscode.
# B1: Mở thư tri_tue_nhan_tao hoặc gõ lệnh: cd tri_tue_nhan_tao (ví dụ hiện ra như này là đúng D:\tri_tue_nhan_tao>)
# B2: Tạo môi trường ảo python: python -m venv env
#     (Khi chạy lệnh trên xong thấy một thư mục env trong thư mục tri_tue_nhan_tao là đúng)
# B3: Kích hoạt môi trường ảo: env/Scripts/activate
#     (thấy chữ env ở đầu trong terminal là đúng. ví dụ: (env) D:\tri_tue_nhan_tao>)
# B4: Tải các thư viện cần thiết: pip install numpy scikit-learn pandas torch transformers sounddevice scipy speechrecognition asyncio edge-tts joblib
# B5: khi terminal đứng ở thư mục tri_tue_nhan_tao kiểu như này ((env) D:\tri_tue_nhan_tao>)
#   chạy lệnh python build_model.py (đợi cho chạy xong build lần đầu khá lâu)
# B6: vào file predict.py
# Có đoạn như này
# ================================================================
# B1: Tải tokenizer & model từ Hugging Face Hub
# tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
# model = AutoModel.from_pretrained("vinai/phobert-base")

# B2: Lưu về thư mục local
# tokenizer.save_pretrained("./phobert-base-offline")
# model.save_pretrained("./phobert-base-offline")
# ================================================================
# Khi đó bôi đen toàn bộ đoạn này và bấm ctrl + /
# Bôi đen toàn bộ đoạn phía sau và bấm ctrl + /

# B7: chạy lệnh trong terminal: python predict.py
#     (nếu thấy có thư mục phobert-base-offline được tạo ra là đúng)
# B8: Xóa đoạn 
# ================================================================
# B1: Tải tokenizer & model từ Hugging Face Hub
# tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
# model = AutoModel.from_pretrained("vinai/phobert-base")

# B2: Lưu về thư mục local
# tokenizer.save_pretrained("./phobert-base-offline")
# model.save_pretrained("./phobert-base-offline")
# ================================================================
# sau đó bôi đen đoạn phía sau sau đó bấm ctrl + /

# B9: chạy python predict.py
# chú ý vào bảng terminal và làm theo đúng yêu cầu mà nó hiện ra
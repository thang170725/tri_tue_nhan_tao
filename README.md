# hướng dẫn setup và run project

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

# B2: Lưu về thư mục localv
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
<!-- from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_true = [...]  # nhãn thật
y_pred = [...]  # nhãn dự đoán

cm = confusion_matrix(y_true, y_pred, labels=unique_labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=unique_labels)
disp.plot(cmap="Blues", xticks_rotation=45)
plt.title("Confusion Matrix - Smart Home Command Classification")
plt.show() -->

<!-- 
==============================
====== CÂY THƯ MỤC ===========
==============================
 -->
.
├── build_model.py
├── chart
│   └── chart.png
├── check_dataset.py
├── dataset1.csv
├── dataset.csv
├── input_sound_processor.py
├── intent_classifier.pkl
├── intent_model_gpu.pt
├── phobert-base-offline
│   ├── added_tokens.json
│   ├── bpe.codes
│   ├── config.json
│   ├── model.safetensors
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── vocab.txt
├── predict.py
├── __pycache__
│   ├── build_model.cpython-310.pyc
│   ├── build_model_v2.cpython-310.pyc
│   └── input_sound_processor.cpython-310.pyc
├── README.md
├── songs
│   ├── 10 MẤT 1 CÒN KHÔNG REMIX.mp3
│   ├── CÓ MÌNH VÀ TA REMIX.mp3
│   ├── KHÓC NƠI TA CƯỜI REMIX.mp3
│   ├── MÌNH LÀ NGƯỜI YÊU CŨ REMIX.mp3
│   ├── NGÀY EM CƯỚI REMIX.mp3
│   └── THAM PHÚ PHỤ BẦN REMIX.mp3
├── vectorizer.pkl
└── version_2
    ├── build_model_v2.py
    ├── intent_model.pt
    ├── label_encoder.pkl
    ├── music_player.py
    ├── predict_v2.py
    ├── __pycache__
    └── weather_api.py
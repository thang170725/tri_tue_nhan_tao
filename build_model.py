"""
    file này dùng để xây dựng mô hình
"""
from sklearn.preprocessing import LabelEncoder                          # dùng để encode nhãn
import pandas as pd                                                     # dùng để đọc và xử lý dataset
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModel
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from sklearn.linear_model import LogisticRegression
class Model:
    def __init__(self, df_path="dataset.csv"):
        self.df = pd.read_csv(df_path)

        self.label_encoder = LabelEncoder()
        self.df["label"] = self.label_encoder.fit_transform(self.df["intent"])

        print("Đang tải phoBERT ...")
        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
        self.model = AutoModel.from_pretrained(
            "vinai/phobert-base", 
            output_attentions = True
        )
        print("phoBERT đã sẵn sàng")

    def train_test_split(self, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(
            self.df['text'], 
            self.df['label'], 
            test_size=test_size, 
            random_state=42, 
            stratify=self.df["label"])
        return X_train.to_list(), X_test.to_list(), y_train.to_list(), y_test.to_list()
    
    def get_sentence_embedding(self, text):
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :] # shape (1, 768)

        return cls_embedding.squeeze().numpy() # dạng (768,)

    def get_train_test_vectors(self):
        X_train, X_test, y_train, y_test = self.train_test_split()
        print("Đang tạo vector cho X_train ...")
        X_train_vectors = [self.get_sentence_embedding(text) for text in X_train]
        print("Đang tạo vertor cho X_train ...")
        X_test_vectors = [self.get_sentence_embedding(text) for text in X_test]
        
        return X_train_vectors, X_test_vectors, y_train, y_test 

    # huấn luyện mô hình (dùng mạng nơ ron)
    def train_model(self, X_train_vectors, y_train):
        clf = MLPClassifier(
            hidden_layer_sizes=(256, 128),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=42
        )
        clf.fit(X_train_vectors, y_train)
        print("Huấn luyên mô hình hoàn tất")
        return clf
    
    def train_model_logistic(self, X_train_vectors, y_train):
        # Khởi tạo mô hình
        clf = LogisticRegression(
            penalty='l2',       # regularization L2
            C=1.0,              # regularization strength
            solver='lbfgs',     # optimizer
            multi_class='auto', # tự động chọn OVR hoặc multinomial
            max_iter=200,       # số vòng lặp tối đa
            random_state=42
        )

        # Huấn luyện
        clf.fit(X_train_vectors, y_train)
        return clf

    #Đánh giá mô hình
    def evaluate(self, clf, X_test_vectors, y_test):
        y_pred =  clf.predict(X_test_vectors)
        print("=== ĐÁNH GIÁ MÔ HÌNH ===")
        print("độ chính xác:", accuracy_score(y_test, y_pred))
        print(
            "báo cáo phân loại:\n", 
            classification_report(
                y_test, 
                y_pred, 
                target_names=self.label_encoder.classes_,
                zero_division=0 # tránh lỗi chia 0 nếu nhãn không xuất hiện
            )
        )

    def save_model(self, clf, model_path="intent_classifier.pkl", encoder_path="label_encoder.pkl"):
        joblib.dump({
            'model': clf,
            'label_encoder': self.label_encoder
        }, model_path)
        # joblib.dump(self.label_encoder, encoder_path)
        print("Đã lưu mô hình vào", model_path)
        print("các nhãn đã được mã hóa: ", list(self.label_encoder.classes_))

if __name__ == "__main__":
    m = Model("dataset1.csv")
    X_train_vec, X_test_vec, y_train, y_test = m.get_train_test_vectors()
    clf = m.train_model(X_train_vec, y_train)
    m.evaluate(clf, X_test_vec, y_test)
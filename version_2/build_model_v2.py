from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, TensorDataset
import joblib
from tqdm import tqdm

'''
========================================================================================
====================== XÂY DỰNG MÔ HÌNH PHÂN LOẠI Ý ĐỊNH (PYTORCH) =====================
========================================================================================
'''

# Dataset cho DataLoader
class IntentDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


# Mạng nơ-ron đơn giản (MLP)
class TorchClassifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super(TorchClassifier, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.net(x)


# Class bao trùm toàn bộ pipeline
class Model:
    def __init__(self, df_path="dataset1.csv", batch_size=16, lr=1e-3, epochs=10):
        self.df = pd.read_csv(df_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Sử dụng thiết bị: {self.device}")

        # Chuẩn bị dữ liệu
        self.vectorizer = CountVectorizer()
        X = self.vectorizer.fit_transform(self.df["text"]).toarray()

        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(self.df["intent"])

        # Chia dữ liệu
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        self.X_test, self.y_test = X_test, y_test

        # Dataset và Dataloader
        self.train_dataset = IntentDataset(X_train, y_train)
        self.test_dataset = IntentDataset(X_test, y_test)
        self.train_loader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True)
        self.test_loader = DataLoader(self.test_dataset, batch_size=batch_size, shuffle=False)

        # Mô hình
        input_size = X.shape[1]
        num_classes = len(self.label_encoder.classes_)
        self.model = TorchClassifier(input_size, num_classes).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.CrossEntropyLoss()

        # Tham số
        self.epochs = epochs

    # ---------------- HUẤN LUYỆN ----------------
    def train(self):
        self.model.train()
        for epoch in range(self.epochs):
            total_loss = 0
            for X_batch, y_batch in tqdm(self.train_loader, desc=f"Epoch {epoch+1}/{self.epochs}"):
                X_batch, y_batch = X_batch.to(self.device), y_batch.to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(X_batch)
                loss = self.criterion(outputs, y_batch)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            print(f"Epoch {epoch+1}/{self.epochs} - Loss: {total_loss/len(self.train_loader):.4f}")

    # ---------------- ĐÁNH GIÁ ----------------
    def evaluate(self):
        self.model.eval()
        y_true, y_pred = [], []
        with torch.no_grad():
            for X_batch, y_batch in self.test_loader:
                X_batch = X_batch.to(self.device)
                outputs = self.model(X_batch)
                preds = torch.argmax(outputs, dim=1)
                y_true.extend(y_batch.numpy())
                y_pred.extend(preds.cpu().numpy())

        acc = accuracy_score(y_true, y_pred)
        print("=== ĐÁNH GIÁ MÔ HÌNH ===")
        print("Độ chính xác:", acc)
        print(classification_report(y_true, y_pred, target_names=self.label_encoder.classes_))

    # ---------------- LƯU MÔ HÌNH ----------------
    def save_model(self, model_path="intent_model.pt", vec_path="vectorizer.pkl", encoder_path="label_encoder.pkl"):
        torch.save(self.model.state_dict(), model_path)
        joblib.dump(self.vectorizer, vec_path)
        joblib.dump(self.label_encoder, encoder_path)
        print(f"✅ Đã lưu mô hình vào {model_path}")
        print(f"✅ Các nhãn: {list(self.label_encoder.classes_)}")

    # ---------------- DỰ ĐOÁN ----------------
    def predict(self, text, model_path="intent_model.pt", vec_path="vectorizer.pkl", encoder_path="label_encoder.pkl"):
        # Load model & encoder
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        self.vectorizer = joblib.load(vec_path)
        self.label_encoder = joblib.load(encoder_path)

        x = self.vectorizer.transform([text]).toarray()
        x_tensor = torch.tensor(x, dtype=torch.float32).to(self.device)

        with torch.no_grad():
            output = self.model(x_tensor)
            pred_id = torch.argmax(output, dim=1).item()
            intent = self.label_encoder.inverse_transform([pred_id])[0]

        print(f"👉 Câu: {text}")
        print(f"🎯 Ý định dự đoán: {intent}")
        return intent


# ---------------- CHẠY THỰC NGHIỆM ----------------
if __name__ == "__main__":
    m = Model("dataset1.csv", epochs=3)
    m.train()
    m.evaluate()
    m.save_model()

    # Thử dự đoán
    m.predict("bật đèn phòng khách")
    m.predict("tắt điều hòa đi")

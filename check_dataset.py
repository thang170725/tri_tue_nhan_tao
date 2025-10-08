'''
    file này để kiểm tra dataset, trực quan hóa dataset, kiểm soát dataset dễ dàng hơn
'''
import pandas as pd

class VisualizationDataset:
    def __init__(self, dataset_path="dataset1.csv"):
        self.df = pd.read_csv(dataset_path)
        # Loại khoảng trắng thừa ở đầu và cuối
        self.df['text'] = self.df['text'].str.strip()

        # Nếu muốn, loại nhiều khoảng trắng giữa các từ
        self.df['text'] = self.df['text'].str.replace(r'\s+', ' ', regex=True)


    def duplicate(self, column='text'):
        print("=== duplicate bắt đầu ===")
        duplicates = self.df[self.df.duplicated(subset=[column], keep=False)]
        print(duplicates)
        print("=== duplicate kết thúc === ")
    
    def counts_intent(self, column='intent'):
        print("=== Đếm số lượng intent bắt đầu === ")
        c = self.df[column].value_counts()
        print(c)
        print("=== Đếm số lượng intent kết thúc === ")

if __name__ == '__main__':
    visual = VisualizationDataset()
    df = visual.df
    visual.duplicate()
    visual.counts_intent()
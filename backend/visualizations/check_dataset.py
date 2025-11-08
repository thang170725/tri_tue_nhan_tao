import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

'''
========================================================================================
====================== CLASS KIỂM TRA DATASET, OUTLIER =================================
========================================================================================
'''
class CheckDataset:
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

'''
========================================================================================
====================== CLASS VẼ BIỂU ĐỒ TRỰC QUAN DỮ LIỆU ==============================
========================================================================================
'''
class VisualChart:
    def __init__(self, dataset_path="dataset1.csv"):
        self.df = pd.read_csv(dataset_path)
        # Tạo thêm cột độ dài câu
        self.df["length"] = self.df["text"].apply(lambda x: len(str(x).split()))

        # tạo figsize 2x2
        self.fig, self.ax = plt.subplots(2, 2, figsize=(12,5))
        self.ax = self.ax.flatten()  # Chuyển thành mảng 1D
        
    '''
    ============================================================================
    ======= BIỂU ĐỒ THỂ HIỆN SỐ LƯỢNG MẪU MỖI LỚP ==============================
    ============================================================================
    ''' 
    def count_plot(self, ax):
        sns.countplot(x='intent', data=self.df, palette='Set2', ax=ax)
        ax.set_title('Phân bố các lệnh (Intent Distribution)')
        ax.tick_params(axis='x', rotation=45)
    '''
    ============================================================================
    ======= BIỂU ĐỒ XEM PHÂN BỐ ĐỘ DÀI CÂU LỆNH ================================
    ============================================================================
    '''
    def histogram_len(self, ax):
        ax.hist(self.df["length"], bins=10, color="skyblue", edgecolor="black")
        ax.set_title("Phân bố độ dài câu lệnh (số từ)")
        ax.set_xlabel("Số từ trong câu")
        ax.set_ylabel("Tần suất")
    '''
    ============================================================================
    ======= BIỂU ĐỒ KIỂM TRA TỪ KHÓA NỔI BẬT TRONG TỪNG LỚP ====================
    ============================================================================
    '''
    def word_cloud(self, ax):
        text = " ".join((self.df["text"]).astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title("Từ khóa phổ biến trong các câu lệnh")
    '''
    ============================================================================
    ======= BIỂU ĐỒ KIỂM TRA MỐI QUAN HỆ GIỮA ĐỘ DÀI CÂU VÀ LOÀI LỆNH ==========
    ============================================================================
    '''
    def box_plot(self, ax):
        sns.boxplot(x="intent", y="length", data=self.df, ax=ax)
        ax.tick_params(rotation=45)
        ax.set_title("Độ dài câu theo từng lệnh")     

'''
============================================================================
======================================= TEST ===============================
============================================================================
'''   
if __name__ == '__main__':
    # run class checkDataset
    # check = CheckDataset()
    # df = check.df
    # check.duplicate()
    # check.counts_intent()

    # run class VisualChart
    chart = VisualChart()
    ax = chart.ax
    chart.count_plot(ax[0])
    chart.histogram_len(ax[1])
    chart.word_cloud(ax[2])
    chart.box_plot(ax[3])
    plt.tight_layout()
    plt.savefig('chart/chart.png')
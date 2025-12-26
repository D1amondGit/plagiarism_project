import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PlagiarismDetector:
    def __init__(self, upload_folder="uploads", report_folder="reports"):
        self.upload_folder = upload_folder
        self.report_folder = report_folder
        self.files = []
        self.contents = []
        self.filenames = []

    def load_files(self):
        """Загружает все .txt файлы из папки uploads"""
        # Ищем все файлы с расширением .txt
        path = os.path.join(self.upload_folder, "*.txt")
        self.files = glob.glob(path)
        
        if len(self.files) < 2:
            return "⚠️ Мало файлов для сравнения. Нужно минимум 2 файла в папке uploads/."

        self.contents = []
        self.filenames = []
        
        for file in self.files:
            # Читаем каждый файл
            with open(file, 'r', encoding='utf-8') as f:
                self.contents.append(f.read())
            # Сохраняем имя файла (например, student1.txt)
            self.filenames.append(os.path.basename(file))
        
        return f"✅ Загружено работ: {len(self.files)}"

    def check_similarity(self):
        """Считает схожесть через TF-IDF и Cosine Similarity"""
        if not self.contents:
            return None

        # 1. Превращаем текст в математические векторы
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.contents)
        
        # 2. Считаем косинусное сходство (от 0 до 1)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        return similarity_matrix

    def generate_report(self, similarity_matrix):
        """Рисует красивую тепловую карту (Heatmap)"""
        if similarity_matrix is None:
            return None
        
        # Создаем таблицу для графика
        df = pd.DataFrame(similarity_matrix, index=self.filenames, columns=self.filenames)
        
        # Настройка графика
        plt.figure(figsize=(10, 8))
        sns.heatmap(df, annot=True, cmap="coolwarm", vmin=0, vmax=1, fmt=".2f")
        plt.title("Матрица схожести работ (Плагиат)")
        
        # Сохраняем картинку
        output_path = os.path.join(self.report_folder, "similarity_matrix.png")
        plt.savefig(output_path)
        plt.close()
        return output_path
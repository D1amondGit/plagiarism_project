import sys
import os
import pytest
import shutil

# Добавляем путь к src, чтобы Python видел наш код
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plagiarism import PlagiarismDetector

# --- ТЕСТЫ ЛОГИКИ (МАТЕМАТИКА) ---

def test_initialization():
    """Проверка: Класс создается с правильными папками"""
    detector = PlagiarismDetector()
    assert detector.upload_folder == "uploads"
    assert detector.report_folder == "reports"

def test_similarity_identical():
    """Проверка: Одинаковые тексты = 100% сходство"""
    detector = PlagiarismDetector()
    # Эмулируем загрузку файлов (без реального чтения с диска)
    detector.filenames = ["file1.txt", "file2.txt"]
    detector.contents = ["Hello world python code", "Hello world python code"]
    
    matrix = detector.check_similarity()
    
    # Сравниваем 1-й файл со 2-м. Должно быть ~1.0
    assert matrix[0][1] > 0.99

def test_similarity_different():
    """Проверка: Разные тексты = почти 0% сходство"""
    detector = PlagiarismDetector()
    detector.filenames = ["file1.txt", "file2.txt"]
    detector.contents = ["Complete difference here", "Absolutno drugie slova"]
    
    matrix = detector.check_similarity()
    
    # Сходство должно быть низким
    assert matrix[0][1] < 0.2

# --- ТЕСТЫ РАБОТЫ С ФАЙЛАМИ (INTEGRATION) ---

def test_load_files_empty():
    """Проверка: Если папка пустая или мало файлов - выдает предупреждение"""
    # Создаем временную пустую папку для теста
    test_dir = "temp_test_uploads"
    os.makedirs(test_dir, exist_ok=True)
    
    detector = PlagiarismDetector(upload_folder=test_dir)
    status = detector.load_files()
    
    # Чистим за собой
    shutil.rmtree(test_dir)
    
    assert "Мало файлов" in status or "не найдены" in status

def test_load_real_files():
    """Проверка: Система реально видит файлы в папке uploads"""
    # Используем настоящую папку uploads, куда ты уже положил файлы
    detector = PlagiarismDetector(upload_folder="uploads")
    
    # Если ты положил туда 2+ файла, метод должен вернуть "Загружено"
    if len(os.listdir("uploads")) >= 2:
        status = detector.load_files()
        assert "Загружено" in status
        assert len(detector.contents) > 0
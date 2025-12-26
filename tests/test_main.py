import sys
import os
import pytest
import numpy as np

# Трюк, чтобы видеть код из папки src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plagiarism import PlagiarismDetector

def test_detector_initialization():
    """Проверка, что класс создается правильно"""
    detector = PlagiarismDetector()
    assert detector.upload_folder == "uploads"

def test_similarity_identical_text():
    """Тест: Одинаковые тексты должны давать 100% сходство"""
    detector = PlagiarismDetector()
    # Подсовываем данные напрямую, минуя чтение файлов
    detector.filenames = ["doc1.txt", "doc2.txt"]
    detector.contents = ["Hello world", "Hello world"]
    
    matrix = detector.check_similarity()
    
    # matrix[0][1] - это сравнение 1-го текста со 2-м. Должно быть 1.0
    assert matrix[0][1] > 0.99

def test_similarity_different_text():
    """Тест: Разные тексты должны давать почти 0% сходство"""
    detector = PlagiarismDetector()
    detector.filenames = ["doc1.txt", "doc2.txt"]
    detector.contents = ["Hello world", "Banana apple orange"]
    
    matrix = detector.check_similarity()
    
    # Сходство должно быть очень маленьким
    assert matrix[0][1] < 0.2
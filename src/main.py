from plagiarism import PlagiarismDetector
import json
import os
from datetime import datetime

def main():
    print("🔍 ЗАПУСК СИСТЕМЫ АНТИПЛАГИАТА...")
    
    # Инициализация
    detector = PlagiarismDetector()
    
    # 1. Загрузка файлов
    status = detector.load_files()
    print(status)
    
    if "Мало файлов" in status:
        return

    # 2. Математический анализ
    matrix = detector.check_similarity()
    
    # 3. Генерация картинки
    image_path = detector.generate_report(matrix)
    print(f"📊 График сохранен: {image_path}")
    
    # 4. Сохранение отчета в JSON (для истории)
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "files_checked": detector.filenames,
        "matrix": matrix.tolist() # Превращаем в список для JSON
    }
    
    json_path = os.path.join("reports", "results.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False)
        
    print(f"📝 Текстовый отчет: {json_path}")
    print("✅ ГOTOВО!")

if __name__ == "__main__":
    main()
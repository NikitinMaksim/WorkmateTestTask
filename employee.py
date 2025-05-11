from typing import List, Dict, Any

class Employee:
    """Класс для хранения данных о сотруднике"""
    def __init__(self, data: Dict[str, Any]):
        # Базовые данные сотрудника
        self.id = data.get('id')  # Уникальный идентификатор
        self.email = data.get('email')  # Адрес электронной почты
        self.name = data.get('name')  # Полное имя сотрудника
        self.department = data.get('department')  # Название отдела
        self.hours_worked = float(data.get('hours_worked', 0))  # Отработанные часы
        
        # Поиск поля с часовой ставкой (может называться по-разному)
        rate_keys = ['hourly_rate', 'rate', 'salary']
        self.hourly_rate = 0
        for key in rate_keys:
            if key in data:
                self.hourly_rate = float(data[key])
                break
    
    @property
    def payout(self) -> float:
        """Рассчитывает общую выплату (часы * ставка)"""
        return self.hours_worked * self.hourly_rate
    
class CSVReader:
    """Класс для чтения CSV файлов без использования библиотеки csv"""
    @staticmethod
    def read_file(file_path: str) -> List[Dict[str, Any]]:
        # Чтение всех строк из файла
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return []  # Пустой файл
        
        # Получаем заголовки из первой строки
        headers = [header.strip() for header in lines[0].split(',')]
        data = []
        
        # Обрабатываем каждую строку данных
        for line in lines[1:]:
            values = [value.strip() for value in line.split(',')]
            if len(values) != len(headers):
                continue  # Пропускаем некорректные строки
            # Собираем словарь {заголовок: значение}
            data.append(dict(zip(headers, values)))
        
        return data